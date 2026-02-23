# Artifact Registry Cron Replicator

## General Overview

This repository provides an easily forkable example of a lightweight Cloud Scheduler -> Cloud Run Job set up to automate cron-based replication between Google Artifact Registry repositories using the new CopyRepository API.

Replication GCP resources are managed by Terraform and a `scripts/deploy.sh` script is provided to deploy the infrastructure and the application, after populating `infra/terraform.tfvars`.

## Project Structure

- `app/`: Contains the FastAPI application codebase for the Cloud Run deployment.
- `infra/`: Contains the Terraform infrastructure-as-code files.

## Prerequisites

- Google Cloud Project with Billing enabled.
- `gcloud` CLI installed and authenticated.
- Terraform CLI installed.
- (Optional) `uv` or `pip` for local Python development.

## Setup Instructions

### 1. Configure Prerequisites

Ensure you have `gcloud` and `terraform` installed and authenticated.

### 2. Configure Variables

Copy the example variables file and populate it with your values:

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars
```

### 3. Deploy

Run the deployment script, which handles infrastructure provisioning and image building:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 4. Verification

Once deployed, the script will output the Cloud Scheduler job status. You can also manually trigger the job via the Cloud Console or CLI:

```bash
gcloud run jobs execute artifact-registry-cron-replicator --region <REGION>
```

## CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yaml`) is included to run linting (`ruff`) and tests (`pytest`) on every push to `main`.

## Local Development

### Cloud Run Job

This project uses `requirements.txt` for Python dependencies.

1. Go into the `app` directory.

```bash
cd app
```

2. Create a virtual environment.

```bash
python3 -m venv .venv
```

3. Activate the virtual environment.

```bash
source .venv/bin/activate
```

4. Install dependencies.

```bash
pip3 install -r requirements.txt ruff pytest pytest-cov pytest-asyncio
```

5. When all done, you can deactivate the virtual environment.

```bash
deactivate
```

#### Code Quality

Ensure the code is formatted and linted before committing:

```bash
ruff check .
ruff format .
```

#### Testing

We follow a Test Driven Development (TDD) approach. To run tests:

```bash
pytest
```

#### Run server locally

Make sure that desired env vars are set either explicitely or via a .env file:

```bash
export SOURCE_REPOSITORY="projects/..."
export DESTINATION_REPOSITORIES='["projects/..."]'
export POLL_OPERATION="false"
export COPY_CONTINUE_ON_SKIPPED_VERSION="false"
export COPY_MAX_VERSION_AGE_DAYS="0"
export COPY_ALL_ATTACHMENTS_INCLUDED="false"
export COPY_ALL_TAGS_EXCLUDED="false"
export DRY_RUN="true"

uvicorn main:app --reload
```
