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
        with patch("client.logger") as mock_logger:
            result = await client.copy_repository("projects/p/locations/l/repositories/d")

            # Verify return value
            assert result == {"name": "operations/dry-run", "done": True}

            # Verify NO HTTP request was made
            mock_http_client.post.assert_not_called()

            # Verify Logging
            # We expect "DRY RUN MODE ENABLED" and payload info
            # Only checking that we logged something indicating dry run
            # because exact string matching might be brittle if we change wording slightly
            # but user asked for "very obvious"
            mock_logger.info.assert_any_call("DRY RUN MODE ENABLED")
            
            # Check for payload log
            # The payload should include behavior
            expected_payload_part = "'continueOnSkippedVersion': True"
            # We can't easily match the whole dictionary string representation in one go without being exact
            # but we can check if any call args contains it
            found_payload = False
            for call in mock_logger.info.call_args_list:
                if str(call) and expected_payload_part in str(call):
                    found_payload = True
                    break
            assert found_payload, "Payload with behavior not found in logs"
