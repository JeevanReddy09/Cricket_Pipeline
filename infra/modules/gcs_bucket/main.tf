resource "google_storage_bucket" "data_bucket" {
  name     = var.bucket_name
  project  = var.project_id
  location = var.location

  # This setting prevents accidental deletion of a bucket with data in it
  force_destroy = false
}