# Artifact Registry Cron Replicator

This repository provides a lightweight Cloud Run application and Terraform configuration to easily set up automated cron-based replication between Google Cloud Artifact Registry repositories using the new `CopyRepository` API.

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

Now that Terraform has created the `cron-replicator` Artifact Registry repository, you can build and push the image.

```bash
# Configure Docker for Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and push the container
docker build -t us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/cron-replicator/replicator:latest .
docker push us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/cron-replicator/replicator:latest
```



### 3. Trigger Cloud Run Deployment (If initial failed)

If the first Terraform apply failed to deploy the Cloud Run service because the image was missing, simply run `terraform apply` again now that the image is pushed.

```bash
cd infra/
terraform apply
```

### 4. Verification
Once deployed, you can navigate to Cloud Scheduler in the GCP Console and click **Force Run** on the `trigger-ar-cron-replication` job.
Check the Cloud Run Logs to ensure the replication triggered successfully.

## Local Development
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
4. Start the server (Requires Environment Variables `SOURCE_REPOSITORY` and `DESTINATION_REPOSITORIES` to be exported):
   ```bash
   export SOURCE_REPOSITORY="projects/..."
   export DESTINATION_REPOSITORIES='["projects/..."]'
   uv run uvicorn main:app --reload
   ```
5. Send a mock trigger request in another terminal window:
   ```bash
   curl -X POST http://localhost:8000/copy
   ```
