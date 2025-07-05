variable "project_id" {
  description = "Your GCP Project ID"
  type        = string
}

variable "region" {
  description = "The region to deploy resources into"
  type        = string
  default     = "us-central1"
}

variable "gcs_bucket_name" {
  description = "The name for the GCS data landing bucket."
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

variable "dataproc_cluster_name" {
  description = "The name of the Dataproc Spark cluster."
  type        = string
  default     = "spark-cluster"
}

variable "dataproc_zone" {
  description = "The zone for the Dataproc cluster."
  type        = string
  default     = "us-central1-a"
}