# Artifact Registry Cron Replicator

## General Overview

This repository provides a lightweight Cloud Run application and Terraform configuration to easily set up automated cron-based replication between Google Cloud Artifact Registry repositories using the new `CopyRepository` API.

## Project Structure

- `app/`: Contains the FastAPI application codebase for the Cloud Run deployment.
- `infra/`: Contains the Terraform infrastructure-as-code files.
- `app/Dockerfile`: Used for building the Cloud Run container.

## Workflow

1. **Fork this repository** to your own GitHub account / organization.
2. **Configure Terraform** variables to match your environment.
3. **Deploy** using the provided instructions, which will take less than 10 minutes.

## Prerequisites
- Google Cloud Project with Billing enabled.
- `gcloud` CLI installed and authenticated.
- Terraform CLI installed.
- (Optional) `uv` for local Python development.

## Setup Instructions

### 1. Deploy Infrastructure via Terraform

Terraform will create the required Artifact Registry repository, the Cloud Run service, and the Cloud Scheduler job. Note: The initial Cloud Run deployment might fail if the container image isn't pushed yet, which is expected.

```bash
cd infra/

# Initialize Terraform plugins
terraform init

# Copy the example variables file
cp terraform.tfvars.example terraform.tfvars

# Open terraform.tfvars in your editor and configure your repositories
# e.g., using nano or vim:
# nano terraform.tfvars

# Review and apply the configuration
terraform plan
terraform apply
```

### 2. Build and push the container image

Now that Terraform has created the `cron-replicator` Artifact Registry repository, you can build and push the image using Google Cloud Build (no local Docker required).

```bash
# Build and push the replicator image.
gcloud builds submit --tag <REGION>-docker.pkg.dev/<YOUR_PROJECT_ID>/cron-replicator/replicator:latest app/

# Update the Cloud Run service to use the new image.
gcloud run services update artifact-registry-cron-replicator \
  --region <REGION> \
  --image <REGION>-docker.pkg.dev/<YOUR_PROJECT_ID>/cron-replicator/replicator:latest
```

### 3. Trigger Cloud Run Deployment (If initial failed)

If the first Terraform apply failed to deploy the Cloud Run Job because the image was missing, simply run `terraform apply` again now that the image is pushed.

```bash
cd infra/
terraform apply
```

### 4. Verification
Once deployed, you can navigate to Cloud Scheduler in the GCP Console and click **Force Run** on the `trigger-ar-cron-replication` job.

Alternatively, you can manually trigger the Cloud Run Job:
```bash
gcloud run jobs execute artifact-registry-cron-replicator --region <REGION>
```

Check the Cloud Run Job execution logs to ensure the replication triggered successfully and the job exited with a success status.

## Development Guidelines

### Dependency Management
This project uses `uv` for Python dependencies. **Do not use `pip`** to manage dependencies in code.
- To add a package: `cd app && uv add <package>`
- To sync dependencies: `cd app && uv sync`

### Code Quality
Ensure the code is formatted and linted before committing:
```bash
cd app
uv run ruff check .
uv run ruff format .
```

### Testing
Tests are located in `app/tests`. We follow a Test Driven Development (TDD) approach.
To run tests:
```bash
cd app
uv run pytest
```

### Maintenance & Synchronization
If you make any changes to environment variables, requirements, or Terraform variables, you **must** update:
1. This `README.md`
2. `infra/terraform.tfvars.example` (Source of truth for Terraform input values)

### Local Development
If you wish to run the FastAPI app locally:

1. Install `uv` dependency manager (https://github.com/astral-sh/uv).
2. Install dependencies:
   ```bash
   cd app && uv sync
   ```
3. Set your ADC credentials locally:
   ```bash
   gcloud auth application-default login
   ```
4. Run the script (Requires Environment Variables `SOURCE_REPOSITORY` and `DESTINATION_REPOSITORIES` to be exported):
   ```bash
   export SOURCE_REPOSITORY="projects/..."
   export DESTINATION_REPOSITORIES='["projects/..."]'
   uv run python main.py
   ```
