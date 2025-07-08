from __future__ import annotations
import pendulum
import logging
import json

from airflow.models.dag import DAG #type: ignore
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator #type: ignore

# --- HARDCODED CONFIGURATION FOR DEV/DEBUG ---
GCP_PROJECT_ID = "cbpl-01"
GCP_REGION = "us-central1"
GCP_CONN_ID = "google_cloud_default"
RAW_BUCKET = "cricket-raw"
PROCESSED_BUCKET = "cricket-processed"

# IMPORTANT: This must match the name of the cluster you created with Terraform
CLUSTER_NAME = "cricket-spark-cluster" 
PYSPARK_SCRIPT_PATH = f"gs://{RAW_BUCKET}/scripts/process_cricket_data.py"

# --- Focused on T20 data only for this test run ---
MATCH_TYPES = [
    {"type": "t20", "input_folder": "t20_json"},
    {"type": "odi", "input_folder": "odi_json"},
    {"type": "test", "input_folder": "test_json"},
]

# --- Debug Log: Print initial config ---
logging.info(f"Using Project: {GCP_PROJECT_ID}, Region: {GCP_REGION}")
logging.info(f"Cluster Name: {CLUSTER_NAME}")


with DAG(
    dag_id="dev_spark_job",
    start_date=pendulum.datetime(2025, 7, 8, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["cricsheet", "dataproc", "spark", "dev"],
) as dag:

    # The loop will only run once for the T20 config
    for config in MATCH_TYPES:
        match_type = config['type']
        
        job_config = {
            "reference": {"project_id": GCP_PROJECT_ID},
            "placement": {"cluster_name": CLUSTER_NAME}, 
            "pyspark_job": {
                "main_python_file_uri": PYSPARK_SCRIPT_PATH,
                "args": [
                    f"gs://{RAW_BUCKET}/{config['input_folder']}/",
                    f"gs://{PROCESSED_BUCKET}/cricsheet_data/",
                    match_type
                ]
            },
        }

        # --- Debug Log: Print the job config before submitting ---
        # Using json.dumps makes the dictionary easy to read in the logs
        logging.info(f"Submitting job for {match_type} with config:")
        logging.info(json.dumps(job_config, indent=2))

        # Create the job submission task
        DataprocSubmitJobOperator(
            task_id=f"submit_spark_job_{match_type}",
            job=job_config,
            region=GCP_REGION,
            project_id=GCP_PROJECT_ID,
            gcp_conn_id=GCP_CONN_ID,
        )