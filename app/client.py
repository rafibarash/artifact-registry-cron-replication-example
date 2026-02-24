import asyncio
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

        api_url = (
            f"https://artifactregistry.googleapis.com/v1/{destination}:copyRepository"
        )

        payload = {
            "sourceRepository": self.settings.source_repository,
            "destinationRepository": destination,
            "behavior": {
                "continueOnSkippedVersion": self.settings.copy_continue_on_skipped,
                "maxVersionAgeDays": self.settings.copy_max_version_age_days,
                "allAttachmentsIncluded": self.settings.copy_all_attachments,
                "allTagsExcluded": self.settings.copy_all_tags_excluded,
            },
        }

        if self.settings.dry_run:
            logger.info(f"DRY RUN: copy to {destination} with payload: {payload}")
            return {"name": "operations/dry-run", "done": True}

        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            op = response.json()
            logger.info(
                f"Triggered copy from {self.settings.source_repository} to "
                f"{destination}: Operation {op.get('name')}"
            )

            if self.settings.poll_operation:
                op_name = op.get("name")
                if op_name:
                    poll_url = f"https://artifactregistry.googleapis.com/v1/{op_name}"
                    # Poll every 15s until done
                    while not op.get("done"):
                        logger.info(f"Polling operation {op_name}...")
                        await asyncio.sleep(15)
                        poll_response = await client.get(poll_url, headers=headers)
                        poll_response.raise_for_status()
                        op = poll_response.json()

            return op
