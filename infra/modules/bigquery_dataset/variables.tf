variable "dataset_id" {
  description = "The ID of the BigQuery dataset."
  type        = string
}

variable "project_id" {
  description = "The GCP Project ID."
  type        = string
}

variable "location" {
  description = "The location for the dataset."
  type        = string
}