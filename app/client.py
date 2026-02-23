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
        # e.g., POST https://artifactregistry.googleapis.com/v1/projects/my-project/locations/us-central1/repositories/my-repo:copyRepository
        api_url = f"https://artifactregistry.googleapis.com/v1/{destination}:copyRepository"

        payload = {
            "sourceRepository": self.settings.source_repository,
            "behavior": {
                "continueOnSkippedVersion": self.settings.copy_continue_on_skipped,
                "maxVersionAgeDays": self.settings.copy_max_version_age_days,
                "allAttachmentsIncluded": self.settings.copy_all_attachments,
                "allTagsExcluded": self.settings.copy_all_tags_excluded,
            },
        }

        if self.settings.dry_run:
            logger.info("DRY RUN MODE ENABLED")
            logger.info(f"Would trigger copy to {destination} with payload: {payload}")
            logger.info(f"API URL: {api_url}")
            return {"name": "operations/dry-run", "done": True}

        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
