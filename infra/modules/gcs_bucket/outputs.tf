
output "name" {
  description = "The name of the GCS data bucket."
  value       = google_storage_bucket.data_bucket.name
}