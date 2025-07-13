# Cricket Analytics Data Pipeline
A comprehensive end-to-end data engineering project that automates the extraction, processing, and analysis of cricket match data from Cricsheet. This pipeline demonstrates modern data engineering practices using Google Cloud Platform, Apache Airflow, Apache Spark, dbt, and Terraform.

🏏 Project Overview
This project builds a production-ready data pipeline that:

Extracts cricket match data from Cricsheet.org with intelligent caching

Processes JSON data into optimized Parquet format using Apache Spark

Transforms raw data into analytical models using dbt

Automates the entire workflow with Apache Airflow

Manages infrastructure as code with Terraform

Visualizes insights through interactive dashboards

## Architecture

Cricsheet.org → Airflow → Spark/Dataproc → BigQuery → dbt → Looker Studio


