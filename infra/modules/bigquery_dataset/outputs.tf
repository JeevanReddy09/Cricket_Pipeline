output "id" {
  description = "The ID of the BigQuery dataset."
  value       = google_bigquery_dataset.dataset.dataset_id
}