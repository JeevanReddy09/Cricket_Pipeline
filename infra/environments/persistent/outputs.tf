output "gcs_bucket_name" {
  description = "The name of the created GCS bucket"
  value       = module.gcs_bucket.name
}

output "bigquery_dataset_id" {
  description = "The ID of the created BigQuery dataset"
  value       = module.bigquery_dataset.id
}

output "service_account_email" {
  description = "The email of the created service account"
  value       = module.service_account.email
} 