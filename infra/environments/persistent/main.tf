provider "google" {
  project = var.project_id
  region  = var.region
}

module "gcs_bucket" {
  source          = "../../modules/gcs_bucket"
  project_id      = var.project_id
  bucket_name     = var.gcs_bucket_name
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