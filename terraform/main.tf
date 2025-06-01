provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = var.zone
  credentials = file("terraform-key.json") 
}

resource "google_compute_instance" "backend_vm" {
  name         = "fullstack-backend"
  machine_type = "e2-medium"
  zone         = var.zone

  tags = ["http-server", "https-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"
    access_config {}  # создаёт внешний IP
  }

  metadata = {
    ssh-keys = "user:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCwV8TG//5CUBSbFpMKzGyAHBR4JF4ZdQsqmxlNQEyrpd12jkjZ8YQSvZ7iWl8vnr2F3BrG1QMJTmC2FFcAQysvNSivTEmWZ9Bj/3B/QHrQbW7RDfyYKLdxhD6ZwG3OsbAz4TPnREMwd7sKY6RVuahVstZlfT3D62P84DynhyP0Lx5qJyvlFp4T2yaNj9y0yOkHaOqJSnW808RUCo2Y3a9CM6/9I5cf1Jj3HdFszmqDPiFrpFIms3SNULFBy+lISj+XEgxTFv86xIi01v4al7GXmsxIi9ugIteaj5Pah/7j60oEUS+X6DIxAk3uGvOKHv+xftFIYUXS9H+vKOexFvPT user@DESKTOP-TGN25KV"
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt update
    sudo apt install -y docker.io git
    sudo systemctl enable docker
    sudo systemctl start docker
    git clone https://github.com/elliaaan/SRE /opt/app
    cd /opt/app/Fullstack-TodoApp
    docker compose up -d
  EOT
}
