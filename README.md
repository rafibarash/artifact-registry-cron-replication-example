# Artifact Registry Cron Replicator

## General Overview

This repository provides a lightweight Cloud Run application and Terraform configuration to easily set up automated cron-based replication between Google Cloud Artifact Registry repositories using the new `CopyRepository` API.

## Project Structure

- `app/`: Contains the FastAPI application codebase for the Cloud Run deployment.
- `infra/`: Contains the Terraform infrastructure-as-code files.
- `app/Dockerfile`: Used for building the Cloud Run container.

## Prerequisites
- Google Cloud Project with Billing enabled.
- `gcloud` CLI installed and authenticated.
- Terraform CLI installed.
- (Optional) `uv` for local Python development.

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

## Security Considerations

- **IAM Permissions**: The Terraform configuration currently grants `roles/artifactregistry.repoAdmin` to the Cloud Run Service Account at the **Project Level**.
    - This is done for simplicity to allow copying to any destination repository in the project.
    - **Recommendation**: For production environments, scope this permission to specific destination repositories using `google_artifact_registry_repository_iam_member`.
- **Secrets**: Ensure `terraform.tfvars` is NOT committed to version control (it is ignored by default).

## CI/CD
A GitHub Actions workflow (`.github/workflows/ci.yaml`) is included to run linting (`ruff`) and tests (`pytest`) on every push to `main`.

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
