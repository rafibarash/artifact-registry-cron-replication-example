import logging

import google.auth
import httpx
from google.auth.transport.requests import Request

from config import Settings

logger = logging.getLogger(__name__)


class CopyRepositoryClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def copy_repository(self, destination: str) -> dict:
        credentials, project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        credentials.refresh(Request())

        # Build AR API endpoint URL
        # e.g., POST https://artifactregistry.googleapis.com/v1/projects/my-project/locations/us-central1/repositories/my-repo:copy
        api_url = f"https://artifactregistry.googleapis.com/v1/{destination}:copy"

        payload = {"sourceRepository": self.settings.source_repository}

        # Add optional config flags to payload based on settings
        if self.settings.copy_continue_on_skipped:
            # Note: API might expect specific boolean fields, assuming standard names.
            pass

        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
