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
    status_codes = []

    async def copy(dest: str) -> None:
        try:
            result = await client.copy_repository(dest)
            operations.append(result)
        except Exception as e:
            error_msg = (
                f"Error triggering copy from {settings.source_repository} "
                f"to {dest}: {e}"
            )
            logger.error(error_msg)
            errors.append(error_msg)

            if isinstance(e, ValueError):
                status_codes.append(502)
            else:
                status_codes.append(500)

    # Run copy operations in parallel. Only waits if poll_operation is enabled.
    tasks = [copy(dest) for dest in settings.destination_repositories]
    await asyncio.gather(*tasks)

    if errors:
        final_status = 502 if 502 in status_codes else 500
        raise HTTPException(
            status_code=final_status,
            detail={"message": "One or more copy operations failed", "errors": errors},
        )

    if settings.poll_operation:
        logger.info("All copy operations successfully completed")
        return CopyResponse(
            message="All copy operations successfully completed",
            operations=operations,
            errors=errors,
        )
    logger.info("All copy operations successfully triggered")
    return CopyResponse(
        message="All copy operations successfully triggered",
        operations=operations,
        errors=errors,
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
