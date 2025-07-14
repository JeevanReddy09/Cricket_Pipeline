import os
import zipfile
import json
import shutil
from datetime import datetime

import requests
from airflow.models.dag import DAG # type: ignore
from airflow.models.variable import Variable # type: ignore
from airflow.operators.trigger_dagrun import TriggerDagRunOperator # type: ignore
from airflow.operators.python import PythonOperator, ShortCircuitOperator # type: ignore
from google.cloud import storage

# Define constants for the data sources and variable keys
CRICSHEET_SOURCES = {
    "odi": {
        "url": "https://cricsheet.org/downloads/odis_json.zip",
        "etag_variable": "cricsheet_odi_etag",
    },
    "test": {
        "url": "https://cricsheet.org/downloads/tests_json.zip",
        "etag_variable": "cricsheet_test_etag",
    },
    "t20": {
        "url": "https://cricsheet.org/downloads/t20s_json.zip",
        "etag_variable": "cricsheet_t20_etag",
    },
}

def check_if_source_updated(url: str, etag_variable_key: str) -> bool:
    """
    Performs a HEAD request to check the ETag of the remote file.
    Compares it with the ETag from the last successful run stored in an Airflow Variable.
    """
    print(f"Checking for updates at {url}...")
    try:
        response = requests.head(url, timeout=30)
        response.raise_for_status()
        new_etag = response.headers.get('ETag')
        
        if not new_etag:
            print("Warning: ETag not found. Proceeding with run.")
            return True

        last_etag = Variable.get(etag_variable_key, default_var=None)
        
        print(f"  - Current ETag: {new_etag}")
        print(f"  - Stored ETag: {last_etag}")

        if new_etag == last_etag:
            print("Source has not changed. Skipping pipeline.")
            return False
        else:
            print("Source has been updated. Proceeding.")
            return True
    except requests.RequestException as e:
        print(f"Error checking source: {e}. Proceeding as a precaution.")
        return True

def process_and_load_data(url: str, match_type: str, etag_variable_key: str):
    """
    Downloads data and uploads it to GCS, checking for existence first.
    On success, it updates the Airflow Variable with the new ETag.
    """
    gcs_bucket_name = "cricket-raw"
    temp_dir = f"/tmp/cricsheet_{match_type}"
    os.makedirs(temp_dir, exist_ok=True)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket_name)

    # Download
    print(f"Downloading {match_type} data from {url}...")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    new_etag = response.headers.get('ETag')
    zip_filename = os.path.join(temp_dir, f"{match_type}.zip")
    with open(zip_filename, 'wb') as f:
        f.write(response.content)

    # Unzip
    unzip_dir = os.path.join(temp_dir, "unzipped")
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)
    
    # Transform and Upload
    upload_folder = f"{match_type}_json"
    print(f"Processing files for gs://{gcs_bucket_name}/{upload_folder}/")
    files_uploaded = 0
    files_skipped = 0
    
    for filename in os.listdir(unzip_dir):
        if not filename.endswith(".json"):
            continue
        
        blob_name = f"{upload_folder}/{filename}"
        blob = bucket.blob(blob_name)
        
        # --- NEW: Check if the file already exists in GCS ---
        if blob.exists():
            files_skipped += 1
            continue
        
        local_file_path = os.path.join(unzip_dir, filename)
        try:
            with open(local_file_path, 'r') as f:
                data = json.load(f)
            
            info_data = data.get('info')
            if info_data:
                blob.upload_from_string(
                    data=json.dumps(info_data, indent=2),
                    content_type='application/json'
                )
                files_uploaded += 1
        except Exception as e:
            print(f"An error occurred with {filename}: {e}")
    
    print("Processing complete.")
    print(f"  - Uploaded: {files_uploaded} new files.")
    print(f"  - Skipped: {files_skipped} existing files.")

    # On success, update the ETag in Airflow Variables
    if new_etag:
        print(f"Updating variable '{etag_variable_key}' with new ETag: {new_etag}")
        Variable.set(key=etag_variable_key, value=new_etag)
    
    # Cleanup
    shutil.rmtree(temp_dir)

with DAG(
    dag_id='raw_data_upload_to_gcs',
    schedule_interval=None,  # Daily at 2 AM
    start_date=datetime(2025, 7, 5),
    catchup=False,
    tags=['cricsheet', 'gcs', 'production'],
    doc_md="""
    ### Cricsheet Pipeline with Full Idempotency
    
    This DAG processes ODI, Test, and T20 data in parallel and includes two layers of idempotency checks:
    
    1.  **Source Check**: Uses an ETag to check if the source .zip file has changed. If not, the entire pipeline for that data type is skipped.
    2.  **Destination Check**: Before uploading a processed JSON file, it checks if a file with the same name already exists in the GCS bucket. If it exists, the individual upload is skipped. This makes the pipeline resilient to partial failures.
    
    **Required Setup**: You must create the following Airflow Variables before running: `cricsheet_odi_etag`, `cricsheet_test_etag`, `cricsheet_t20_etag`.
    
    **Pipeline Flow**: This DAG triggers the transform cricket data DAG upon successful completion.
    """
) as dag:

    # --- Create the parallel task branches ---
    process_tasks = []
    for match_type, config in CRICSHEET_SOURCES.items():
        
        check_task = ShortCircuitOperator(
            task_id=f'check_if_source_updated_{match_type}',
            python_callable=check_if_source_updated,
            op_kwargs={
                'url': config["url"],
                'etag_variable_key': config["etag_variable"]
            }
        )
        
        process_task = PythonOperator(
            task_id=f'process_and_load_data_{match_type}',
            python_callable=process_and_load_data,
            op_kwargs={
                'url': config["url"],
                'match_type': match_type,
                'etag_variable_key': config["etag_variable"]
            }
        )
        
        # Define the dependency chain for each branch
        check_task >> process_task
        process_tasks.append(process_task)

    # --- Trigger the transform cricket data DAG after all processing is complete ---
    trigger_transform_dag = TriggerDagRunOperator(
        task_id='trigger_transform_cricket_data',
        trigger_dag_id='spark_jobs_and_dbt_trigger',
        wait_for_completion=False,
        poke_interval=60,
        trigger_rule='all_success'
    )
    
    # All process tasks should complete before triggering the next DAG
    for task in process_tasks:
        task >> trigger_transform_dag