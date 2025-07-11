resource "google_bigquery_table" "external_table" {
  dataset_id          = var.dataset_id
  table_id            = var.table_id
  project             = var.project_id
  deletion_protection = false

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    source_uris   = var.source_uris
  }
} 