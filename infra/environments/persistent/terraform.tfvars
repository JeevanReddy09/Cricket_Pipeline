project_id                = "cbpl-01"
gcs_raw_bucket_name       = "cricket-raw"
gcs_processed_bucket_name = "cricket-processed"
bq_dataset_name           = "cricket_data"
account_id                = "cricket-pipeline-sa"
display_name              = "Cricket Pipeline Service Account"

# External table configuration for Parquet files from Spark job
external_table_name        = "processed_cricket_matches"
external_table_source_uris = ["gs://cricket-processed/cricsheet_data/*"] 