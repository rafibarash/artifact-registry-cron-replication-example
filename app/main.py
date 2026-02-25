import asyncio
import logging
import sys
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from client import CopyRepositoryClient
from config import get_settings

app = FastAPI(title="Artifact Registry Cron Replicator")
logger = logging.getLogger(__name__)


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

    tasks = [client.copy_repository(dest) for dest in settings.destination_repositories]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for dest, result in zip(settings.destination_repositories, results, strict=False):
        if isinstance(result, Exception):
            error_msg = (
                f"Error triggering copy from {settings.source_repository} "
                f"to {dest}: {result}"
            )
            logger.error(error_msg)
            errors.append(error_msg)
        else:
            operations.append(result)

    if errors and not operations:
        raise HTTPException(
            status_code=500,
            detail={"message": "All copy operations failed", "errors": errors},
        )

    return CopyResponse(
        message="Copy operations triggered", operations=operations, errors=errors
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        result = asyncio.run(run_copy_job())
        if result.errors and not result.operations:
            sys.exit(1)
    except Exception:
        logger.exception("Job failed with unexpected error")
        sys.exit(1)
