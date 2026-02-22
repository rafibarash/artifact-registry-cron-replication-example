# Implementation Plan: Implement Core Infrastructure and FastAPI Application

## Phase 1: Project Scaffolding and Initial Setup

- [ ] Task: Create the basic directory structure for the project (`app`, `terraform`, `.github/workflows`).
- [ ] Task: Initialize the Python project with `uv` and add initial dependencies (`fastapi`, `uvicorn`, `pytest`, `httpx`, `google-auth`, `pydantic`).
- [ ] Task: Create a basic "Hello World" FastAPI application in `app/main.py` to verify the setup.
- [ ] Task: Conductor - User Manual Verification 'Project Scaffolding and Initial Setup' (Protocol in workflow.md)

## Phase 2: Terraform Infrastructure

- [ ] Task: Write failing tests for the Terraform configuration (e.g., using `terratest` or by asserting plan output).
- [ ] Task: Implement the Terraform configuration for the Service Account.
- [ ] Task: Implement the Terraform configuration for the Artifact Registry repository.
- [ ] Task: Implement the Terraform configuration for the Cloud Run Job.
- [ ] Task: Implement the Terraform configuration for the Cloud Scheduler Job.
- [ ] Task: Run `terraform apply` to provision the resources.
- [ ] Task: Conductor - User Manual Verification 'Terraform Infrastructure' (Protocol in workflow.md)

## Phase 3: FastAPI Application Logic

- [ ] Task: Write failing tests for the `/copy` endpoint.
- [ ] Task: Implement the `/copy` endpoint in `app/main.py`.
- [ ] Task: Write failing tests for the `CopyRepository` API call logic.
- [ ] Task: Implement the logic to call the `CopyRepository` API using `httpx`, mocking the external API.
- [ ] Task: Implement configuration loading from environment variables using Pydantic.
- [ ] Task: Ensure all new code has >80% test coverage.
- [ ] Task: Conductor - User Manual Verification 'FastAPI Application Logic' (Protocol in workflow.md)

## Phase 4: Containerization and CI/CD

- [ ] Task: Write the `Dockerfile` to containerize the FastAPI application.
- [ ] Task: Build the Docker image locally to verify the `Dockerfile`.
- [ ] Task: Create the GitHub Actions workflow file (`.github/workflows/ci.yaml`).
- [ ] Task: Implement the linting and testing jobs in the CI workflow.
- [ ] Task: Conductor - User Manual Verification 'Containerization and CI/CD' (Protocol in workflow.md)
