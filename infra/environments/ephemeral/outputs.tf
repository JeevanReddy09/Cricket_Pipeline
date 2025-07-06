output "dataproc_cluster_name" {
  description = "The name of the created Dataproc cluster"
  value       = module.dataproc_cluster.cluster_name
}

output "dataproc_cluster_id" {
  description = "The ID of the created Dataproc cluster"
  value       = module.dataproc_cluster.cluster_id
}

output "dataproc_master_instance_names" {
  description = "The master instance names of the Dataproc cluster"
  value       = module.dataproc_cluster.master_instance_names
}

output "dataproc_worker_instance_names" {
  description = "The worker instance names of the Dataproc cluster"
  value       = module.dataproc_cluster.worker_instance_names
} 