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

## Development Guidelines

### Dependency Management

This project uses `requirements.txt` for Python dependencies.

- To install dependencies: `cd app && pip install -r requirements.txt`

### Code Quality

Ensure the code is formatted and linted before committing:

```bash
cd app
ruff check .
ruff format .
```

### Testing

Tests are located in `app/tests`. We follow a Test Driven Development (TDD) approach.
To run tests:

```bash
cd app
pytest
```

### Maintenance & Synchronization

If you make any changes to environment variables, requirements, or Terraform variables, you **must** update:

1. This `README.md`
2. `infra/terraform.tfvars.example` (Source of truth for Terraform input values)

### Local Development

If you wish to run the FastAPI app locally:

1. Create and activate a virtual environment:

   ```bash
   cd app
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your ADC credentials locally:

   ```bash
   gcloud auth application-default login
   ```

4. Run the script (Requires Environment Variables `SOURCE_REPOSITORY` and `DESTINATION_REPOSITORIES` to be exported):

   ```bash
   export SOURCE_REPOSITORY="projects/..."
   export DESTINATION_REPOSITORIES='["projects/..."]'
   python main.py
   ```
