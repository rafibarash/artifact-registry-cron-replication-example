import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_copy_endpoint_success(monkeypatch):
    from config import Settings

    mock_settings = Settings(source_repository="src", destination_repositories=["dest"])
    monkeypatch.setattr("main.get_settings", lambda: mock_settings)

    # Mock the CopyRepositoryClient methods so we don't hit real APIs
    from client import CopyRepositoryClient

    async def mock_copy_repository(self, destination: str):
        return {"name": f"operations/mock-{destination.split('/')[-1]}", "done": False}

    monkeypatch.setattr(CopyRepositoryClient, "copy_repository", mock_copy_repository)

    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/copy")

    assert response.status_code == 200
    data = response.json()
    assert "operations" in data
    # Ensure there's an operation recorded for each destination repo
    assert len(data["operations"]) >= 1


@pytest.mark.asyncio
async def test_copy_endpoint_failure(monkeypatch):
    from config import Settings

    mock_settings = Settings(source_repository="src", destination_repositories=["dest"])
    monkeypatch.setattr("main.get_settings", lambda: mock_settings)

    from client import CopyRepositoryClient

    async def mock_copy_repository_failure(self, destination: str):
        raise ValueError("Simulated copy failure")

    monkeypatch.setattr(
        CopyRepositoryClient, "copy_repository", mock_copy_repository_failure
    )

    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/copy")

    assert response.status_code == 500
