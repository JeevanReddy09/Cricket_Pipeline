provider "google" {
  project = var.project_id
  region  = var.region
}

# Raw data bucket for incoming cricket data
module "gcs_raw_bucket" {
  source          = "../../modules/gcs_bucket"
  project_id      = var.project_id
  bucket_name     = var.gcs_raw_bucket_name
  location        = var.region
}

# Processed data bucket for Spark job output
module "gcs_processed_bucket" {
  source          = "../../modules/gcs_bucket"
  project_id      = var.project_id
  bucket_name     = var.gcs_processed_bucket_name
  location        = var.region
}

module "bigquery_dataset" {
  source = "../../modules/bigquery_dataset"

  dataset_id = var.bq_dataset_name
  project_id = var.project_id
  location   = var.region
}

module "service_account" {
  source       = "../../modules/service_account"
  account_id   = var.account_id
  display_name = var.display_name
  project_id   = var.project_id
}

# External table for processed cricket match data (Parquet files from Spark job)
module "cricket_matches_external_table" {
  source     = "../../modules/bigquery_external_table"
  depends_on = [module.bigquery_dataset, module.gcs_processed_bucket]

  project_id  = var.project_id
  dataset_id  = module.bigquery_dataset.id
  table_id    = var.external_table_name
  source_uris = var.external_table_source_uris
} 