from unittest.mock import AsyncMock, patch

import pytest

from client import CopyRepositoryClient
from config import Settings


@pytest.fixture
def mock_settings():
    return Settings(
        source_repository="projects/my-project/locations/us-central1/repositories/source-repo",
        destination_repositories=[
            "projects/my-project/locations/us-central1/repositories/dest-repo"
        ],
    )


@pytest.mark.asyncio
@patch("client.google.auth.default")
async def test_copy_repository_success(mock_google_auth, mock_settings):
    # Setup mock auth
    mock_credentials = AsyncMock()
    mock_credentials.token = "fake-token"
    mock_google_auth.return_value = (mock_credentials, "my-project")

    # Needs to mock httpx.AsyncClient
    with patch("client.httpx.AsyncClient") as mock_http_client_class:
        from unittest.mock import MagicMock

        mock_http_client = AsyncMock()
        mock_http_client_class.return_value.__aenter__.return_value = mock_http_client

        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            "name": "operations/12345",
            "done": False,
        }
        mock_http_client.post.return_value = mock_post_response

        client = CopyRepositoryClient(mock_settings)
        result = await client.copy_repository(mock_settings.destination_repositories[0])

        assert result.get("name") == "operations/12345"
        mock_http_client.post.assert_called_once()
        args, kwargs = mock_http_client.post.call_args
        assert kwargs["json"]["sourceRepository"] == mock_settings.source_repository
