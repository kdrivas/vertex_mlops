resource "google_artifact_registry_repository" "pred-api-container" {
  location      = "us-central1"
  repository_id = "pred-api-container"
  description   = "Price model container"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository" "pred-package-container" {
  location      = "us-central1"
  repository_id = "pred-package-container"
  description   = "Price model package container"
  format        = "DOCKER"
}