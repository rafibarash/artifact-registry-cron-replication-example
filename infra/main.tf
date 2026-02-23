terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable Required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudscheduler.googleapis.com",
    "artifactregistry.googleapis.com"
  ])
  service            = each.key
  disable_on_destroy = false
}

# Artifact Registry to hold the Cloud Run container image
resource "google_artifact_registry_repository" "app_repo" {
  location      = var.region
  repository_id = "cron-replicator"
  description   = "Docker repo for the artifact registry cron replicator app"
  format        = "DOCKER"
  depends_on    = [google_project_service.apis]
}

# Cloud Run Service Account
resource "google_service_account" "runner" {
  account_id   = "ar-cron-replicator"
  display_name = "AR Cron Replicator Service Account"
}

# Grant Cloud Run SA read/write permissions to Artifact Registry
# Warning: Roles may need adjusting if cross-project copying is required.
resource "google_project_iam_member" "ar_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.repoAdmin"
  member  = "serviceAccount:${google_service_account.runner.email}"
}

# Cloud Run Service (Assumes image is built and pushed before applying or dynamically passed.
# For simplicity, using a dummy image initially, which you overwrite in CI/CD or manuall build step).
# Cloud Run Job
resource "google_cloud_run_v2_job" "default" {
  name     = "artifact-registry-cron-replicator"
  location = var.region

  template {
    template {
      service_account = google_service_account.runner.email
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app_repo.repository_id}/replicator:latest"
        
        env {
          name  = "SOURCE_REPOSITORY"
          value = var.source_repo
        }
        env {
          name  = "DESTINATION_REPOSITORIES"
          # Convert list to string representation for Python to parse or use just one if logic changes, 
          # but current logic parses it? No, app usage needs check. 
          # Config says `destination_repositories: list[str]`. 
          # Pydantic can parse JSON string or list if env var is properly formatted.
          # `jsonencode` produces `["a", "b"]` which pydantic should parse as list.
          value = jsonencode(var.destination_repos)
        }
        env {
          name  = "POLL_OPERATION"
          value = tostring(var.poll_operation)
        }
        env {
          name  = "COPY_CONTINUE_ON_SKIPPED"
          value = tostring(var.continue_on_skipped_version)
        }
        env {
          name  = "COPY_MAX_VERSION_AGE_DAYS"
          value = tostring(var.max_version_age_days)
        }
        env {
          name  = "COPY_ALL_ATTACHMENTS"
          value = tostring(var.all_attachments_included)
        }
        env {
          name  = "COPY_ALL_TAGS_EXCLUDED"
          value = tostring(var.all_tags_excluded)
        }
      }
    }
  }
  depends_on = [google_project_iam_member.ar_writer]
}

# Cloud Scheduler SA (needs permission to invoke Cloud Run Job)
resource "google_service_account" "invoker" {
  account_id   = "ar-cron-invoker"
  display_name = "AR Cron Replicator Invoker"
}

resource "google_cloud_run_v2_job_iam_member" "invoker_binding" {
  project  = google_cloud_run_v2_job.default.project
  location = google_cloud_run_v2_job.default.location
  name     = google_cloud_run_v2_job.default.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.invoker.email}"
}

# Cloud Scheduler Job
resource "google_cloud_scheduler_job" "job" {
  name             = "trigger-ar-cron-replication"
  description      = "Trigger the replication job on a schedule"
  schedule         = var.schedule
  time_zone        = "Etc/UTC"
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.default.name}:run"
    
    oauth_token {
      service_account_email = google_service_account.invoker.email
    }
  }
  depends_on = [google_cloud_run_v2_job_iam_member.invoker_binding]
}
