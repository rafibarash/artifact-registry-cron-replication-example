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

resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudscheduler.googleapis.com",
    "artifactregistry.googleapis.com"
  ])
  service            = each.key
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "app_repo" {
  location      = var.region
  repository_id = "cron-replicator"
  description   = "Docker repo for the artifact registry cron replicator app"
  format        = "DOCKER"
  depends_on    = [google_project_service.apis]
}

resource "google_service_account" "runner" {
  account_id   = "ar-cron-replicator"
  display_name = "AR Cron Replicator Service Account"
}

# Grant Cloud Run SA read permissions to Source Repository
resource "google_artifact_registry_repository_iam_member" "source_reader" {
  project    = split("/", var.source_repo)[1]
  location   = split("/", var.source_repo)[3]
  repository = split("/", var.source_repo)[5]
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.runner.email}"
}

# Grant Cloud Run SA writer permissions to Destination Repositories
resource "google_artifact_registry_repository_iam_member" "dest_writer" {
  for_each   = toset(var.destination_repos)
  project    = split("/", each.value)[1]
  location   = split("/", each.value)[3]
  repository = split("/", each.value)[5]
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.runner.email}"
}

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
        env {
          name  = "DRY_RUN"
          value = tostring(var.dry_run)
        }
      }
    }
  }
  depends_on = [
    google_artifact_registry_repository_iam_member.source_reader,
    google_artifact_registry_repository_iam_member.dest_writer
  ]
}

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

# Keep outputs which are read by scripts/deploy.sh
output "artifact_registry_repo_url" {
  description = "The URL of the Artifact Registry repository"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app_repo.repository_id}"
}

output "cloud_run_job_name" {
  description = "Name of the Cloud Run Job"
  value       = google_cloud_run_v2_job.default.name
}
