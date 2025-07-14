# Cricsheet Data Engineering Pipeline

An end-to-end data engineering pipeline for processing and analyzing cricket match data from Cricsheet.org, built with modern cloud technologies.

## Table of Contents

* [Project Overview](#project-overview)
* [Architecture](#architecture)

  * [Data Flow](#data-flow)
* [Tools & Technologies](#tools--technologies)
* [Setup](#setup)

  * [Prerequisites](#prerequisites)
  * [Step 1: Create and Configure GCP Project](#step-1-create-and-configure-gcp-project)
  * [Step 2: Clone the Repository](#step-2-clone-the-repository)
  * [Step 3: Install Local Dependencies](#step-3-install-local-dependencies)
  * [Step 4: Configure GCP Authentication](#step-4-configure-gcp-authentication)
  * [Step 5: Deploy Persistent Infrastructure](#step-5-deploy-persistent-infrastructure)
  * [Step 6: Grant Roles to the Service Account](#step-6-grant-roles-to-the-service-account)
  * [Step 7: Configure and Run Airflow](#step-7-configure-and-run-airflow)
* [Running the Automated Pipeline](#running-the-automated-pipeline)
* [Analytics and Visualization](#analytics-and-visualization)

## Project Overview

**Business Problem:** Understand cricket’s evolution through data-driven insights, including format growth, strategic trends, and venue analytics.

**Solution:** An automated ELT pipeline that ingests raw JSON match data from Cricsheet.org, processes and transforms it into analytics-ready tables in BigQuery, and delivers interactive dashboards.

**Impact:** Enables automated analysis of 8,000+ matches across formats, providing insights into global evolution and strategic trends in cricket.

The core objective is to transform raw, nested JSON data into clean, structured, and analytics-ready tables in a data warehouse. The architecture follows a modern ELT (Extract, Load, Transform) pattern with multiple distinct stages, each managed by its own Airflow DAG for modularity and resilience.

## Architecture

The pipeline follows a modern ELT pattern, with each stage managed by its own Airflow DAG for modularity and resilience.

![Architecture Diagram](path/to/architecture-diagram.png)

### Data Flow

* **Extraction:** An Airflow DAG fetches new match data from Cricsheet.org using ETag caching and uploads raw JSON to a GCS bucket.
* **Processing:** A second DAG creates an ephemeral Dataproc cluster to run a Spark job that flattens and cleans the data, writing Parquet files to a processed GCS bucket.
* **Loading:** BigQuery external tables provide direct access to processed Parquet files.
* **Transformation:** A final DAG runs dbt models to build staging and analytical tables in BigQuery.
* **Visualization:** Data marts connect to Looker Studio for interactive dashboards.

## Tools & Technologies

* **Orchestration:** Apache Airflow
* **Processing:** Apache Spark on Google Dataproc
* **Transformation:** dbt (data build tool)
* **Storage:** Google Cloud Storage, Google BigQuery
* **Infrastructure:** Terraform (Infrastructure as Code)
* **Languages:** Python, SQL
* **Containerization:** Docker, Docker Compose

## Setup

### Prerequisites

* Google Cloud Platform account with billing enabled
* Docker & Docker Compose
* Python 3.8+ & pip
* Terraform 1.0+
* Git

### Step 1: Create and Configure GCP Project

1. **Create a new project** (replace `your-unique-project-id`):

   ```bash
   ```

gcloud projects create your-unique-project-id

````
2. **Set the project**:
   ```bash
gcloud config set project your-unique-project-id
````

### Step 2: Clone the Repository
```bash
git clone https://github.com/yourusername/cricket-analytics.git
cd cricket-analytics
````

### Step 3: Install Local Dependencies

```bash
pip install dbt-bigquery
```

### Step 4: Configure GCP Authentication

```bash
gcloud auth application-default login
```

### Step 5: Deploy Persistent Infrastructure

```bash
cd infra/environments/persistent
terraform init
terraform apply
```

This creates:

* GCS buckets (`cricket-raw`, `cricket-processed`)
* A BigQuery dataset (`cricket_data`)
* External BigQuery table(s)
* IAM service account for the pipeline

### Step 6: Grant Roles to the Service Account

1. **Retrieve the service account email**:

   ```bash
terraform output service\_account\_email
````


2. **Grant roles** (replace `SA_EMAIL` and `YOUR_PROJECT_ID`):
   ```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/dataproc.editor"
````

3. **Download service account key**:

   ```bash
gcloud iam service-accounts keys create credentials.json&#x20;
\--iam-account=SA\_EMAIL
````

### Step 7: Configure and Run Airflow
1. **Move credentials**:
   ```bash
mkdir -p airflow/google
mv credentials.json airflow/google/
````

2. **Verify `docker-compose.yaml` mounts**:

   ```yaml

volumes:

* ./dags\:/opt/airflow/dags
* ./logs\:/opt/airflow/logs
* ../dbt:/opt/airflow/dbt
* ./google:/opt/airflow/google

````
3. **Set Airflow Variables** in the Airflow UI (`http://localhost:8080`):
   - `cricsheet_odi_etag`
   - `cricsheet_test_etag`
   - `cricsheet_t20_etag`
4. **Build and start Airflow**:
   ```bash
cd airflow
docker-compose build
docker-compose up -d
````

## Running the Automated Pipeline

1. Trigger the **raw\_upload\_to\_gcs** DAG in Airflow UI.
2. **raw\_upload\_to\_gcs** triggers **transform\_cricket\_data\_dag**.
3. **transform\_cricket\_data\_dag** runs Spark on Dataproc and writes Parquet to GCS.
4. **transform\_cricket\_data\_dag** triggers **dbt\_run\_cricket\_models**.
5. **dbt\_run\_cricket\_models** updates staging and analytics tables in BigQuery.

## Analytics and Visualization

### Analytics Performed (dbt Models)

* **Format Growth Trends:** Matches per format by year
* **Toss Strategy Evolution:** Bat vs. field decisions over time
* **Venue Utilization:** Stadium match counts

### Visualization in Looker Studio

Connect your BigQuery tables (e.g., `format_growth_trends`) to Looker Studio for interactive dashboards.



