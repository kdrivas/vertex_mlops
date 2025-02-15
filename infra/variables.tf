variable "credentials_file" {
  description = "Path to the GCP credentials JSON file"
  type        = string
}

variable "project_id" {
  description = "The existing GCP project that will be used"
  type        = string
}

variable "region" {
  description = "The default region for the project"
  type        = string
  default     = "us-central1"
}
