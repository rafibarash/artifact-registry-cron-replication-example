# Initial Concept

A tool that can be run periodically (e.g. via cron) to
replicate container images from one Artifact Registry repository to
another. The tool should support:

*   Synchronizing all images from a source repository to a destination
    repository. The destination should contain the exact same set of
    tags and images as the source.
*   Dry-run mode to see what operations would be performed without
    actually performing them.
*   The tool should be written in Go.
*   The tool should be containerized and runnable as a container
    image.
*   The tool should be configurable via command-line flags and/or
    environment variables.
*   The tool should support authentication to Artifact Registry using
    Google Application Default Credentials.
*   The tool should be able to handle large repositories with many
    images and tags.
*   The tool should be able to handle repositories in different
    projects and locations.
*   The tool should be able to handle repositories with different
    formats (e.g. Docker, Maven, etc.).
*   The tool should have good test coverage.
*   The tool should have good documentation.
*   The tool should be easy to use and configure.
*   The tool should be reliable and robust.
*   The tool should be secure.
*   The tool should be maintainable and extensible.
*   The tool should be performant.
*   The tool should be cost-effective.
*   The tool should be observable with metrics and logging.
*   The tool should be scalable.
*   The tool should be portable.
*   The tool should be flexible.
*   The tool should be composable.
*   The tool should be declarative.
*   The tool should be idempotent.
*   The tool should be stateless.

---

# Product Guide: Artifact Registry Cron Replicator

## 1. Vision
To provide customers with a simple, forkable GitHub repository that enables easy setup of cron-based replication between Artifact Registry repositories using the new `CopyRepository` API.

## 2. Target Audience
*   **Google Cloud Customers:** Users of Artifact Registry who need a straightforward, automated way to replicate repositories.
*   **DevOps Engineers & SREs:** Who will configure and manage the replication jobs as part of their cloud infrastructure.

## 3. Core Components & User Experience

*   **Fork-and-Configure Workflow:** A user forks the repository, updates a configuration file, and runs setup scripts.
*   **Configuration File:** The repository will contain a configuration file where users define:
    *   GCP Project ID.
    *   The single source (leader) Artifact Registry repository (assumed to exist).
    *   An array of one or more destination (follower) Artifact Registry repositories.
*   **Infrastructure as Code:** The repository will include scripts to provision all necessary Google Cloud resources:
    *   **Artifact Registry Repository:** To host the container image for the replication job.
    *   **Cloud Run Job:** The containerized job that performs the replication.
    *   **Cloud Scheduler:** A cron job to trigger the Cloud Run job on a defined schedule.

## 4. Technical Implementation

*   **Application:** A lightweight **Python FastAPI** server that receives a POST request to trigger the replication.
*   **Configuration:** The Cloud Run job will be configured via environment variables. These variables will directly map to the fields in the `CopyRepositoryRequest` API, such as `source_repository`, `destination_repository`, `dry_run`, etc.
    *   All optional behavior fields (e.g., `destination_exists_behavior`, `max_version_age`) will be unset by default, using the API's default behavior.
*   **Core Logic:** When triggered, the `/copy` endpoint will iterate through the list of destination repositories and invoke the `CopyRepository` API for each one, passing the environment variables from its configuration.
    *   The project's documentation will guide users on how to set variables like `max_version_age` to perform incremental copies after the initial sync.
*   **Authentication:** The Cloud Run job will use its attached service account and Application Default Credentials to authenticate.

## 5. Guiding Principles

*   **Simplicity:** The solution is designed for ease of use, minimizing the steps required to set up replication.
*   **Declarative Setup:** Users define *what* to replicate in the config file; scripts handle the setup.
*   **Immediate Value:** This repository is intended as a working, out-of-the-box example to help customers use the `CopyRepository` API immediately.