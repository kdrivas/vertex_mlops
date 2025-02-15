# Ideally other project have to be created.
data "google_project" "gcp_project" {
  project_id       = var.project_id
}

resource "google_project_service" "services" {
  for_each = toset([
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "compute.googleapis.com",
    "storage.googleapis.com",
    "serviceusage.googleapis.com",
  ])
  project = data.google_project.gcp_project.project_id
  service = each.key
}
