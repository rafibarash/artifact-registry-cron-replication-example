variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy cron-replication resources"
  type        = string
}

variable "source_repo" {
  description = "The Artifact Registry repository to copy from"
  type        = string
}

variable "destination_repos" {
  description = "List of Artifact Registry repositories to copy to"
  type        = list(string)
}

variable "dry_run" {
  description = "Run in dry run mode"
  type        = bool
  default     = false
}

variable "schedule" {
  description = "Cron schedule for triggering the copy job. If omitted, the job will have to be triggered manually."
  type        = string
  default     = ""
}

variable "poll_operation" {
  description = "Poll the copy operation(s) until completion"
  type        = bool
  default     = false
}

variable "timeout" {
  description = "Execution timeout for the Cloud Run Job. If polling is enabled, this should be longer than the expected copy time. See https://docs.cloud.google.com/run/docs/configuring/task-timeout"
  type        = string
  default     = "600s"
}

variable "disable_source_repo_reader" {
  description = "Whether to disable granting the runner SA reader IAM permission on the source repository. If set to true, you must manually grant the permission."
  type        = bool
  default     = false
}

variable "continue_on_skipped_version" {
  description = "Continue repo copies even if a version is skipped due to a version-scoped error"
  type        = bool
  default     = false
}

variable "max_version_age_days" {
  description = "Only copy versions updated/created within these days (0 = no limit)"
  type        = number
  default     = 0
}

variable "all_attachments_included" {
  description = "Include all attachments"
  type        = bool
  default     = false
}

variable "all_tags_excluded" {
  description = "Exclude all tags"
  type        = bool
  default     = false
}

