variable "project_id" {
  description = "The GCP Project ID."
  type        = string
}

variable "region" {
  description = "The GCP region to deploy cron-replication resources."
  type        = string
}

variable "source_repo" {
  description = "The Artifact Registry repository to copy from."
  type        = string
}

variable "destination_repos" {
  description = "The list of Artifact Registry repositories to copy to"
  type        = list(string)
}

variable "schedule" {
  description = "The cron schedule for triggering replication. Default is once a day."
  type        = string
  default     = "12 * * * *"  # Noon every day
}

variable "poll_operation" {
  description = "Whether to poll the Copy operation until completion"
  type        = bool
  default     = false
}

variable "continue_on_skipped_version" {
  description = "Continue copying even if a specific version is skipped due to non-transient errors"
  type        = bool
  default     = false
}

variable "max_version_age_days" {
  description = "If set to > 0, only versions updated/created within the specified number of days will be copied."
  type        = number
  default     = 0
}

variable "all_attachments_included" {
  description = "Include all attachments from the source artifact"
  type        = bool
  default     = false
}

variable "all_tags_excluded" {
  description = "Exclude all tags from the source artifact"
  type        = bool
  default     = false
}

variable "dry_run" {
  description = "Whether to run in dry run mode"
  type        = bool
  default     = false
}

