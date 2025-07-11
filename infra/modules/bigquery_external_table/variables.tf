variable "project_id" {
  description = "The GCP Project ID."
  type        = string
}

variable "dataset_id" {
  description = "The ID of the BigQuery dataset where the table will be created."
  type        = string
}

variable "table_id" {
  description = "The ID of the BigQuery table."
  type        = string
}

variable "source_uris" {
  description = "A list of GCS URIs pointing to Parquet files from Spark job output."
  type        = list(string)
} 