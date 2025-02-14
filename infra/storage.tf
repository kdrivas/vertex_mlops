resource "google_storage_bucket" "artifacts-bucket" {
 name          = "vertex-artifacts-bucket"
 location      = "us-central1"
 storage_class = "STANDARD"
}