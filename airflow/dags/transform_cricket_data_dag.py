from __future__ import annotations
import pendulum
import logging

from airflow.models.dag import DAG # type: ignore
from airflow.providers.google.cloud.operators.dataproc import ( # type: ignore
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
)
from airflow.operators.python import PythonOperator # type: ignore
from airflow.operators.trigger_dagrun import TriggerDagRunOperator # type: ignore
from google.cloud import storage

# --- Configuration ---
GCP_PROJECT_ID = "cbpl-01"
GCP_REGION = "us-central1"
GCP_CONN_ID = "google_cloud_default"
RAW_BUCKET = "cricket-raw"
PROCESSED_BUCKET = "cricket-processed"
CLUSTER_NAME = "ephemeral-cricket-cluster" # Use ephemeral name
PYSPARK_SCRIPT_PATH = f"gs://{RAW_BUCKET}/scripts/process_cricket_data.py"

# Simplified, cost-effective cluster configuration using E2 machines
CLUSTER_CONFIG = {
    "master_config": {"num_instances": 1, "machine_type_uri": "e2-standard-4", 
            "disk_config": {
            "boot_disk_type": "pd-standard",
            "boot_disk_size_gb": 30
        }},
    "worker_config": {"num_instances": 2, "machine_type_uri": "e2-standard-2", 
            "disk_config": {
            "boot_disk_type": "pd-standard",
            "boot_disk_size_gb": 30
        }},
    "software_config": {"image_version": "2.1-debian11"},
}

MATCH_TYPES = [
    {"type": "t20", "input_folder": "t20_json"},
    {"type": "odi", "input_folder": "odi_json"},
    {"type": "test", "input_folder": "test_json"},
]

# --- Minimal Logging Function ---
def log_files_processed(match_type: str, input_path: str):
    """Counts and logs the number of JSON files processed."""
    try:
        client = storage.Client()
        bucket_name, prefix = input_path.replace("gs://", "").split("/", 1)
        blobs = client.list_blobs(bucket_name, prefix=prefix)
        json_file_count = sum(1 for blob in blobs if blob.name.endswith('.json'))
        logging.info(f"Spark job for '{match_type}' processed {json_file_count} JSON files from {input_path}")
    except Exception as e:
        logging.error(f"Could not count files for {match_type} in {input_path}. Error: {e}")

# --- DAG Definition ---
with DAG(
    dag_id="spark_jobs_and_dbt_trigger",
    start_date=pendulum.datetime(2025, 7, 8, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["cricsheet", "dataproc", "spark", "production"],
    description="Automates Dataproc cluster creation, runs Spark jobs, deletes the cluster, and triggers dbt models.",
) as dag:

    # 1. Create the Dataproc cluster
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster",
        project_id=GCP_PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=GCP_REGION,
        cluster_name=CLUSTER_NAME,
        gcp_conn_id=GCP_CONN_ID,
    )

    # 2. Define a list to hold the final logging tasks for dependency setting
    final_log_tasks = []

    # 3. Loop to create Spark job and logging tasks for each match type
    for config in MATCH_TYPES:
        match_type = config["type"]
        input_path = f"gs://{RAW_BUCKET}/{config['input_folder']}/"
        output_path = f"gs://{PROCESSED_BUCKET}/cricsheet_data/"

        # Submit the Spark job
        submit_spark_job = DataprocSubmitJobOperator(
            task_id=f"run_spark_job_{match_type}",
            job={
                "reference": {"project_id": GCP_PROJECT_ID},
                "placement": {"cluster_name": CLUSTER_NAME},
                "pyspark_job": {
                    "main_python_file_uri": PYSPARK_SCRIPT_PATH,
                    "args": [input_path, output_path],
                },
            },
            region=GCP_REGION,
            project_id=GCP_PROJECT_ID,
            gcp_conn_id=GCP_CONN_ID,
        )

        # Log the number of files processed for this job
        log_processed_files = PythonOperator(
            task_id=f"log_files_processed_{match_type}",
            python_callable=log_files_processed,
            op_kwargs={"match_type": match_type, "input_path": input_path},
        )
        
        # Define dependencies for this loop
        create_cluster >> submit_spark_job >> log_processed_files
        final_log_tasks.append(log_processed_files)

    # 4. Delete the Dataproc cluster after all jobs are done
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_dataproc_cluster",
        project_id=GCP_PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        region=GCP_REGION,
        gcp_conn_id=GCP_CONN_ID,
        trigger_rule="all_done",  # Ensures cluster is deleted even if jobs fail
    )
    
    # Set the final dependency: all logging tasks must finish before deleting the cluster
    for task in final_log_tasks:
        task >> delete_cluster

    # 5. Trigger the dbt DAG after successful completion
    trigger_dbt_dag = TriggerDagRunOperator(
        task_id='trigger_dbt_run',
        trigger_dag_id='dbt_run_models',
        wait_for_completion=False,
        poke_interval=60,
        trigger_rule='all_success'
    )
    
    # Delete cluster should complete before triggering dbt DAG
    delete_cluster >> trigger_dbt_dag
