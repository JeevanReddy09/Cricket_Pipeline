output "gcs_raw_bucket_name" {
  description = "The name of the created GCS raw data bucket"
  value       = module.gcs_raw_bucket.name
}

output "gcs_processed_bucket_name" {
  description = "The name of the created GCS processed data bucket"
  value       = module.gcs_processed_bucket.name
}

output "bigquery_dataset_id" {
  description = "The ID of the created BigQuery dataset"
  value       = module.bigquery_dataset.id
}

output "service_account_email" {
  description = "The email of the created service account"
  value       = module.service_account.email
}

output "external_table_id" {
  description = "The ID of the external table"
  value       = module.cricket_matches_external_table.table_id
}

output "external_table_self_link" {
  description = "The self link of the external table"
  value       = module.cricket_matches_external_table.self_link
} 