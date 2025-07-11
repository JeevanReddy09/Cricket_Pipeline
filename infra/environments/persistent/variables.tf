variable "project_id" {
  description = "Your GCP Project ID"
  type        = string
}

variable "region" {
  description = "The region to deploy resources into"
  type        = string
  default     = "us-central1"
}

variable "gcs_raw_bucket_name" {
  description = "The name for the GCS raw data landing bucket."
  type        = string
}

variable "gcs_processed_bucket_name" {
  description = "The name for the GCS processed data bucket (Spark job output)."
  type        = string
}

variable "bq_dataset_name" {
  description = "The name for the BigQuery dataset."
  type        = string
  default     = "raw_data"
}

variable "account_id" {
  description = "The ID of the service account."
  type        = string
}

variable "display_name" {
  description = "The display name of the service account."
  type        = string
}

# External table variables for Parquet files from Spark job
variable "external_table_name" {
  description = "The name of the external table."
  type        = string
  default     = "processed_cricket_matches"
}

variable "external_table_source_uris" {
  description = "List of GCS URIs pointing to Parquet files created by Spark job."
  type        = list(string)
} 