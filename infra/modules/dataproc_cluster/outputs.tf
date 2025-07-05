output "cluster_name" {
  description = "The name of the Dataproc cluster."
  value       = google_dataproc_cluster.spark_cluster.name
}

output "cluster_id" {
  description = "The ID of the Dataproc cluster."
  value       = google_dataproc_cluster.spark_cluster.id
}

output "cluster_config" {
  description = "The configuration of the Dataproc cluster."
  value       = google_dataproc_cluster.spark_cluster.cluster_config
}

output "master_instance_names" {
  description = "List of master instance names."
  value       = google_dataproc_cluster.spark_cluster.cluster_config[0].master_config[0].instance_names
}

output "worker_instance_names" {
  description = "List of worker instance names."
  value       = google_dataproc_cluster.spark_cluster.cluster_config[0].worker_config[0].instance_names
}

output "bucket" {
  description = "The associated GCS bucket."
  value       = google_dataproc_cluster.spark_cluster.cluster_config[0].bucket
} 