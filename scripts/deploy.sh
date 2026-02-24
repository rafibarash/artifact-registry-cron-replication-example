#!/bin/bash
set -e

# 1. Check prerequisites
if ! command -v terraform &> /dev/null || ! command -v gcloud &> /dev/null; then
    echo "Error: terraform and gcloud must be installed."
    exit 1
fi

if [ ! -f "infra/terraform.tfvars" ]; then
    echo "Error: infra/terraform.tfvars not found."
    echo "Please copy 'infra/terraform.tfvars.example' to 'infra/terraform.tfvars' and populate it."
    exit 1
fi

echo "Initializing Terraform..."
cd infra
terraform init

echo "Creating Artifact Registry Repository..."
terraform apply -target=google_artifact_registry_repository.app_repo

echo "Getting Repository URL..."
REPO_URL=$(terraform output -raw artifact_registry_repo_url 2>/dev/null || echo "")

if [ -z "$REPO_URL" ]; then
    echo "Error: Could not detect repository URL from Terraform output."
    exit 1
fi

IMAGE_TAG="${REPO_URL}/replicator:latest"

echo "Building and Pushing image to ${IMAGE_TAG}..."
cd ../app
gcloud builds submit --tag "${IMAGE_TAG}" .

echo "Deploying remaining infrastructure..."
cd ../infra
terraform apply

echo "Deployment Complete!"
