provider "google" {
  project = var.project_id
  region  = var.region
}

module "dataproc_cluster" {
  source       = "../../modules/dataproc_cluster"
  cluster_name = var.dataproc_cluster_name
  project_id   = var.project_id
  region       = var.region
  zone         = var.dataproc_zone
} 