variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "sre-final-461604"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

variable "credentials_file" {
  description = "Path to the service account JSON file"
  type        = string
  default     = "../terraform-key.json"
}
