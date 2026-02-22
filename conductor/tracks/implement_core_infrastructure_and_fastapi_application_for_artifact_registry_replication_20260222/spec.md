# Specification: Implement Core Infrastructure and FastAPI Application

## 1. Overview
This track will establish the foundational infrastructure and the core FastAPI application for the Artifact Registry Cron Replicator. The goal is to create a runnable, containerized application and the necessary cloud resources to support it, based on the definitions in `product.md` and `tech-stack.md`.

## 2. Infrastructure (Terraform)
The following Google Cloud resources will be provisioned using Terraform:

*   **Service Account:** A dedicated IAM Service Account for the Cloud Run job with appropriate permissions to interact with Artifact Registry.
*   **Artifact Registry Repository:** A repository to store the Docker image of the FastAPI application.
*   **Cloud Run Job:** A job configured to run the containerized FastAPI application. It will be triggered by the Cloud Scheduler.
*   **Cloud Scheduler Job:** A cron job scheduled to trigger the Cloud Run job.

The Terraform configuration will be structured to be easily configurable by users who fork the repository.

## 3. FastAPI Application (Python)
A lightweight FastAPI application will be created with the following components:

*   **`main.py`:** The main application entry point.
*   **`/copy` endpoint:** A POST endpoint that, when triggered, will initiate the repository copy process.
*   **Core Logic:** The application will read environment variables for source and destination repositories and use `httpx` to make calls to the `CopyRepository` API.
*   **Configuration:** The application will be configurable via environment variables, as described in `product.md`.
*   **Dependencies:** `fastapi`, `uvicorn`, `pytest`, `httpx`, `google-auth`, `pydantic`. These will be managed by `uv`.

## 4. Containerization (Docker)
A `Dockerfile` will be created to build a container image for the FastAPI application. The image will be based on a slim Python base image.

## 5. CI/CD (GitHub Actions)
A basic GitHub Actions workflow will be set up to:
*   Install dependencies using `uv`.
*   Run linting and formatting checks.
*   Execute the test suite using `pytest`.
*   (Future task, not in this track) Build and push the Docker image to Artifact Registry.

## 6. Definition of Done
*   Terraform code successfully provisions all specified resources.
*   The FastAPI application is containerized and can be run locally.
*   The `/copy` endpoint is functional (in a mocked environment).
*   Unit tests for the core application logic are implemented with >80% coverage.
*   The GitHub Actions workflow successfully completes all defined steps.
