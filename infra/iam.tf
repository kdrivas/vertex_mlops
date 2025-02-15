locals {
  github_sa_roles = [
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountUser",
    "roles/cloudbuild.builds.builder",
    "roles/cloudfunctions.developer",
  ]
  kfp_pipeline_sa_roles = [
    "roles/aiplatform.user",
    "roles/storage.admin",
    "roles/iam.serviceAccountUser",
    "roles/logging.logWriter",
  ]
}

resource "google_service_account" "github_sa" {
  account_id   = "github-sa"
  display_name = "Service Account for Github"
}

# Assign IAM roles to the service account
resource "google_project_iam_member" "sa_roles" {
  for_each = toset(local.github_sa_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.github_sa.email}"
}

resource "google_service_account" "kfp_sa" {
  account_id   = "kfp-sa"
  display_name = "Service Account for Vertex pipelines"
}

# Assign IAM roles to the service account
resource "google_project_iam_member" "kfp_pipeline_sa_roles" {
  for_each = toset(local.kfp_pipeline_sa_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.kfp_sa.email}"
}