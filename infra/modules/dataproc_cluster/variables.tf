variable "cluster_name" {
  description = "The name of the Dataproc cluster."
  type        = string
}

variable "project_id" {
  description = "The GCP Project ID."
  type        = string
}

variable "region" {
  description = "The GCP region for the cluster."
  type        = string
}

variable "zone" {
  description = "The GCP zone for the cluster."
  type        = string
}

variable "image_version" {
  description = "The image version for the cluster."
  type        = string
  default     = "2.0-debian10"
}

variable "master_machine_type" {
  description = "The machine type for the master node."
  type        = string
  default     = "e2-standard-4"
}

variable "master_boot_disk_size_gb" {
  description = "The boot disk size in GB for the master node."
  type        = number
  default     = 30
}

variable "worker_count" {
  description = "The number of worker nodes."
  type        = number
  default     = 2
}

variable "worker_machine_type" {
  description = "The machine type for the worker nodes."
  type        = string
  default     = "e2-standard-4"
}

variable "worker_boot_disk_size_gb" {
  description = "The boot disk size in GB for the worker nodes."
  type        = number
  default     = 30
}

variable "preemptible_worker_count" {
  description = "The number of preemptible worker nodes."
  type        = number
  default     = 0
}

variable "preemptible_boot_disk_size_gb" {
  description = "The boot disk size in GB for the preemptible worker nodes."
  type        = number
  default     = 30
}

variable "network" {
  description = "The network for the cluster."
  type        = string
  default     = "default"
}

variable "subnetwork" {
  description = "The subnetwork for the cluster."
  type        = string
  default     = ""
}

variable "service_account" {
  description = "The service account for the cluster."
  type        = string
  default     = ""
}

variable "tags" {
  description = "Network tags for the cluster."
  type        = list(string)
  default     = []
}

variable "labels" {
  description = "Labels to apply to the cluster."
  type        = map(string)
  default     = {}
} 