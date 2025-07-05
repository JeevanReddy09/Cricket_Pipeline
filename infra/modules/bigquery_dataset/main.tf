resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.dataset_id
  project                    = var.project_id
  location                   = var.location
  delete_contents_on_destroy = false # Safety setting for production
}