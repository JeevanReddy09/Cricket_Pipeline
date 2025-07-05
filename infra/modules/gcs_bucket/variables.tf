
variable "bucket_name" {
  description = "The name of the GCS bucket."
  type        = string
}

variable "project_id" {
  description = "The GCP Project ID."
  type        = string
}

variable "location" {
  description = "The location/region for the bucket."
  type        = string
}