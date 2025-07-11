output "table_id" {
  description = "The ID of the BigQuery external table."
  value       = google_bigquery_table.external_table.table_id
}

output "self_link" {
  description = "The URI of the created resource."
  value       = google_bigquery_table.external_table.self_link
}

output "table_reference" {
  description = "Fully qualified table reference for use in queries."
  value       = "${var.project_id}.${var.dataset_id}.${var.table_id}"
} 