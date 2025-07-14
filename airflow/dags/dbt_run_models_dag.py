from __future__ import annotations
import pendulum
from airflow.operators.bash import BashOperator # type: ignore
from airflow.models.dag import DAG # type: ignore   

# Define the paths inside the Airflow container.
DBT_PROJECT_DIR = "/opt/airflow/dbt/cricket_analytics"


with DAG(
    dag_id="dbt_run_models",
    start_date=pendulum.datetime(2025, 7, 11, tz="UTC"),
    schedule=None, # This DAG is triggered by the spark_jobs_and_dbt_trigger DAG
    catchup=False,
    tags=["cricsheet", "dbt", "production"],
    description="Runs dbt models on processed cricket data. Triggered by the transform cricket data DAG.",
) as dag:
    
    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        # This command navigates to your dbt project and executes 'dbt run'
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR}"
    )