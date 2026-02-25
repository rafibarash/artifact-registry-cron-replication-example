from unittest.mock import AsyncMock, MagicMock, patch

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
    mock_credentials = MagicMock()
    mock_credentials.token = "fake-token"
    mock_google_auth.return_value = (mock_credentials, "my-project")

    # Needs to mock httpx.AsyncClient
    with patch("client.httpx.AsyncClient") as mock_http_client_class:
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


@pytest.mark.asyncio
@patch("client.google.auth.default")
async def test_copy_repository_payload_structure(mock_google_auth, mock_settings):
    # Setup mock auth
    mock_credentials = MagicMock()
    mock_credentials.token = "fake-token"
    mock_google_auth.return_value = (mock_credentials, "my-project")

    # Override settings to ensure all flags are set for verification
    mock_settings.copy_continue_on_skipped = True
    mock_settings.copy_max_version_age_days = 7
    mock_settings.copy_all_attachments = True
    mock_settings.copy_all_tags_excluded = True

    with patch("client.httpx.AsyncClient") as mock_http_client_class:
        mock_http_client = AsyncMock()
        mock_http_client_class.return_value.__aenter__.return_value = mock_http_client

        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"name": "operations/test"}
        mock_http_client.post.return_value = mock_post_response

        client = CopyRepositoryClient(mock_settings)
        await client.copy_repository("projects/p/locations/l/repositories/d")

        mock_http_client.post.assert_called_once()
        _, kwargs = mock_http_client.post.call_args
        payload = kwargs["json"]

        assert payload["sourceRepository"] == mock_settings.source_repository
        assert "behavior" in payload
        behavior = payload["behavior"]
        assert behavior["continueOnSkippedVersion"] is True
        assert behavior["maxVersionAgeDays"] == 7
        assert behavior["allAttachmentsIncluded"] is True
        assert behavior["allTagsExcluded"] is True


@pytest.mark.asyncio
@patch("client.google.auth.default")
async def test_copy_repository_dry_run(mock_google_auth, mock_settings):
    # Setup mock auth
    mock_credentials = MagicMock()
    mock_credentials.token = "fake-token"
    mock_google_auth.return_value = (mock_credentials, "my-project")

    # Enable DRY_RUN
    mock_settings.dry_run = True
    # Ensure some behavior flags are set to verify payload completeness
    mock_settings.copy_continue_on_skipped = True

    with patch("client.httpx.AsyncClient") as mock_http_client_class:
        mock_http_client = AsyncMock()
        mock_http_client_class.return_value.__aenter__.return_value = mock_http_client

        client = CopyRepositoryClient(mock_settings)

        # Capture logs
        with patch("client.logger"):
            result = await client.copy_repository(
                "projects/p/locations/l/repositories/d"
            )

            # Verify return value
            assert result == {"name": "operations/dry-run", "done": True}

            # Verify NO HTTP request was made
            mock_http_client.post.assert_not_called()


@pytest.mark.asyncio
@patch("client.google.auth.default")
@patch("client.asyncio.sleep", new_callable=AsyncMock)
async def test_copy_repository_with_polling(
    mock_sleep, mock_google_auth, mock_settings
):
    mock_credentials = MagicMock()
    mock_credentials.token = "fake-token"
    mock_google_auth.return_value = (mock_credentials, "my-project")

    mock_settings.poll_operation = True

    with patch("client.httpx.AsyncClient") as mock_http_client_class:
        mock_http_client = AsyncMock()
        mock_http_client_class.return_value.__aenter__.return_value = mock_http_client

        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            "name": "operations/test",
            "done": False,
        }
        mock_http_client.post.return_value = mock_post_response

        mock_get_response_1 = MagicMock()
        mock_get_response_1.status_code = 200
        mock_get_response_1.json.return_value = {
            "name": "operations/test",
            "done": False,
        }

        mock_get_response_2 = MagicMock()
        mock_get_response_2.status_code = 200
        mock_get_response_2.json.return_value = {
            "name": "operations/test",
            "done": True,
        }

        mock_http_client.get.side_effect = [mock_get_response_1, mock_get_response_2]

        client = CopyRepositoryClient(mock_settings)
        result = await client.copy_repository("projects/p/locations/l/repositories/d")

        assert result.get("done") is True
        assert mock_http_client.get.call_count == 2
        assert mock_sleep.call_count == 2


@pytest.mark.asyncio
@patch("client.google.auth.default")
@patch("client.asyncio.sleep", new_callable=AsyncMock)
async def test_copy_repository_with_polling_failure(
    mock_sleep, mock_google_auth, mock_settings
):
    mock_credentials = MagicMock()
    mock_credentials.token = "fake-token"
    mock_google_auth.return_value = (mock_credentials, "my-project")

    mock_settings.poll_operation = True

    with patch("client.httpx.AsyncClient") as mock_http_client_class:
        mock_http_client = AsyncMock()
        mock_http_client_class.return_value.__aenter__.return_value = mock_http_client

        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            "name": "operations/test-fail",
            "done": False,
        }
        mock_http_client.post.return_value = mock_post_response

        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "name": "operations/test-fail",
            "done": True,
            "error": {"message": "Permission denied"},
        }
        mock_http_client.get.return_value = mock_get_response

        client = CopyRepositoryClient(mock_settings)
        with pytest.raises(ValueError, match="Operation operations/test-fail failed"):
            await client.copy_repository("projects/p/locations/l/repositories/d")

        assert mock_http_client.post.call_count == 1
        assert mock_http_client.get.call_count == 1
