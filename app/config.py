from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Required parameters
    source_repository: str
    destination_repositories: list[str]

    # Optional parameters and behavior overrides
    copy_continue_on_skipped: bool = False
    copy_max_version_age_days: int = 0
    copy_all_attachments: bool = False
    copy_all_tags_excluded: bool = False
    poll_operation: bool = False
    dry_run: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
    )


def get_settings() -> Settings:
    return Settings()
