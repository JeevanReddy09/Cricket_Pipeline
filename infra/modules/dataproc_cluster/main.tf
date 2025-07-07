resource "google_dataproc_cluster" "spark_cluster" {
  name     = var.cluster_name
  project  = var.project_id
  region   = var.region

  cluster_config {
    # Software configuration
    software_config {
      image_version = var.image_version
      optional_components = ["ZEPPELIN", "JUPYTER", "ANACONDA"]
    }

    endpoint_config {
      enable_http_port_access = true
    }
  
    # Master node configuration
    master_config {
      num_instances = 1
      machine_type  = var.master_machine_type
      disk_config {
        boot_disk_type    = "pd-standard"
        boot_disk_size_gb = var.master_boot_disk_size_gb
      }
    }

    # Worker node configuration  
    worker_config {
      num_instances = var.worker_count
      machine_type  = var.worker_machine_type
      disk_config {
        boot_disk_type    = "pd-standard"
        boot_disk_size_gb = var.worker_boot_disk_size_gb
      }
    }

    # Preemptible worker configuration (optional)
    preemptible_worker_config {
      num_instances = var.preemptible_worker_count
      disk_config {
        boot_disk_type    = "pd-standard"
        boot_disk_size_gb = var.preemptible_boot_disk_size_gb
      }
    }

    # GCE cluster configuration
    gce_cluster_config {
      zone = var.zone
      
      # Service account
      service_account = var.service_account
      service_account_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]

      # Tags for firewall rules
      tags = var.tags
    }
  }

  # Labels for resource management
  labels = var.labels
} 