# Cricsheet Data Engineering Pipeline
This project demonstrates a complete, end-to-end data engineering pipeline built on modern cloud technologies. It ingests raw cricket match data from Cricsheet, processes it using Apache Spark on an ephemeral Dataproc cluster, models it for analytics using dbt, and prepares it for visualization. The entire process is automated and orchestrated with Apache Airflow.

## 🏏 Project Overview

**Business Problem**: Understanding cricket's evolution through data-driven insights including format growth, strategic trends, and venue analytics.

**Solution**: An automated data pipeline that processes cricket match data from Cricsheet.org, transforms it into analytical models, and delivers insights through interactive dashboards.

**Impact**: Enables automated analysis of 8,000+ cricket matches across formats, providing insights into cricket's global evolution and strategic trends.

The core objective is to transform raw, nested JSON data into clean, structured, and analytics-ready tables in a data warehouse. The architecture follows a modern ELT (Extract, Load, Transform) pattern with multiple distinct stages, each managed by its own Airflow DAG for modularity and resilience.

## 🛠️ Tools & Technologies

**Data Engineering:**
- **Orchestration**: Apache Airflow (containerized)
- **Processing**: Apache Spark on Google Dataproc
- **Transformation**: dbt (data build tool)
- **Storage**: Google Cloud Storage, BigQuery
- **Infrastructure**: Terraform (Infrastructure as Code)

**Data Pipeline:**
- **Source**: Cricsheet JSON files with ETag caching
- **Processing**: JSON to Parquet conversion
- **Analytics**: Staging and mart models
- **Visualization**: Looker Studio dashboards

**Development:**
- **Languages**: Python, SQL
- **Version Control**: Git, GitHub
- **Containerization**: Docker, Docker Compose


### Data Flow:
1. **Extraction**: Airflow DAGs with intelligent ETag caching
2. **Processing**: Spark jobs on ephemeral Dataproc clusters
3. **Loading**: External tables in BigQuery
4. **Transformation**: dbt staging and analytical models
5. **Visualization**: Interactive dashboards

## Prerequisites

Google Cloud Platform account with billing enabled

Docker & Docker Compose installed

Python 3.8+

Terraform 1.0+

Git for version control

**Clone repository**

git clone https://github.com/yourusername/cricket-analytics.git


**Set up GCP authentication**

gcloud auth application-default login
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

**Deploy persistent infrastructure first**

cd infra/environments/persistent
terraform init
terraform plan
terraform apply

 This creates:
 - GCS buckets (cricket-raw, cricket-processed)
 - BigQuery datasets
 - External tables
 - Service accounts and IAM roles

**Create service account with required permissions**

gcloud iam service-accounts create cricket-analytics-sa \
    --display-name="Cricket Analytics Service Account"

**Grant necessary roles**

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:cricket-analytics-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:cricket-analytics-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:cricket-analytics-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/dataproc.editor"

**Download service account key**

gcloud iam service-accounts keys create credentials.json \
    --iam-account=cricket-analytics-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

**Move to appropriate directory**

#Docker-compose buiold creates a directory named google
mv credentials.json airflow/google/

**Required Airflow Variables Setup**

Navigate to Airflow UI → Admin → Variables and create the following:

Variable Key		    Description
cricsheet_odi_etag		ETag for ODI data caching
cricsheet_test_etag		ETag for Test data caching
cricsheet_t20_etag		ETag for T20 data caching


## Running the Automated Pipeline
The pipeline is designed to run automatically from end to end.

Initiate the Pipeline: Trigger the first DAG, raw_upload_to_gcs, from the Airflow UI at http://localhost:8080.

**Automated Orchestration:**

Upon successful completion, the raw_upload_to_gcs DAG will automatically trigger the transform_cricket_data_dag.

The transform_cricket_data_dag will create a Dataproc cluster, run the Spark job, and delete the cluster.

Upon successful completion, it will trigger the final dbt_run_cricket_models DAG.

The dbt_run_cricket_models DAG will execute dbt run to update all the analytics tables in BigQuery.

You can monitor the entire process from the Airflow UI, watching as each DAG triggers the next, creating a fully automated, event-driven data pipeline.