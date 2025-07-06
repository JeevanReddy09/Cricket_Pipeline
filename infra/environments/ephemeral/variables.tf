variable "project_id" {
  description = "Your GCP Project ID"
  type        = string
}

variable "region" {
  description = "The region to deploy resources into"
  type        = string
  default     = "us-central1"
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