import logging
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from client import CopyRepositoryClient
from config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Artifact Registry Cron Replicator")


class CopyResponse(BaseModel):
    message: str
    operations: list[dict[str, Any]]
    errors: list[str]


@app.post("/copy", response_model=CopyResponse)
async def trigger_copy():
    return await run_copy_job()


async def run_copy_job() -> CopyResponse:
    settings = get_settings()
    client = CopyRepositoryClient(settings)

    operations = []
    errors = []

    dest_len = len(settings.destination_repositories)
    logger.info(
        f"Triggering copy from {settings.source_repository} to {dest_len} destinations"
    )

    for dest in settings.destination_repositories:
        try:
            result = await client.copy_repository(dest)
            operations.append(result)
            logger.info(f"Triggered copy to {dest}: Operation {result.get('name')}")
        except httpx.HTTPError as e:
            error_msg = f"HTTP error triggering copy to {dest}: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error triggering copy to {dest}: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)

    if errors and not operations:
        # If all failed, for the script we might want to exit non-zero,
        # but for now we'll just return the response and log.
        # When running as a script, we can check this response.
        if __name__ == "__main__":
            logger.error("All copy operations failed")
            # We could sys.exit(1) here if desired, but let's allow the caller to decide.
        else:
             raise HTTPException(
                status_code=500,
                detail={"message": "All copy operations failed", "errors": errors},
            )

    return CopyResponse(
        message="Copy operations triggered", operations=operations, errors=errors
    )


if __name__ == "__main__":
    import asyncio
    import sys

    try:
        result = asyncio.run(run_copy_job())
        # If run as script, we might want to exit with error if all failed
        if result.errors and not result.operations:
             sys.exit(1)
    except Exception as e:
        logger.exception("Job failed with unexpected error")
        sys.exit(1)

