resource "google_compute_firewall" "allow_flask" {
  name    = "allow-flask"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }

  direction     = "INGRESS"
  priority      = 1000
  target_tags   = ["http-server"]
  source_ranges = ["0.0.0.0/0"]
}
resource "google_compute_firewall" "allow_grafana" {
  name    = "allow-grafana"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["3000"]
  }

  direction     = "INGRESS"
  priority      = 1000
  target_tags   = ["http-server"]
  source_ranges = ["0.0.0.0/0"]
}
resource "google_compute_firewall" "allow_prometheus" {
  name    = "allow-prometheus"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["9090"]
  }

  direction     = "INGRESS"
  priority      = 1000
  target_tags   = ["http-server"]
  source_ranges = ["0.0.0.0/0"]
}
resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5000", "3000", "9090"]
  }

  target_tags = ["http-server"]
  direction   = "INGRESS"
  source_ranges = ["0.0.0.0/0"]
}
