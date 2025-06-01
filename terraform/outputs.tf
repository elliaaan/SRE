output "instance_ip" {
  description = "External IP address of the backend VM"
  value       = google_compute_instance.backend_vm.network_interface[0].access_config[0].nat_ip
}


output "backend_ip" {
  value = google_compute_instance.backend_vm.network_interface[0].access_config[0].nat_ip
}
