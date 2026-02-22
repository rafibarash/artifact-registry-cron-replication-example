# Development Plan: Artifact Registry Cron Replicator

## Phase 1: Project Setup & Tooling
- [ ] Initialize Python project using `uv` (FastAPI, uvicorn, pydantic, pydantic-settings, httpx, google-auth, pytest, pytest-cov, ruff)
- [ ] Configure `pyproject.toml` toolings (ruff linting/formatting rules, coverage thresholds)
- [ ] Ensure project passes initial static analysis

## Phase 2: Core Domain Logic & Configuration
- [ ] Create data models for configuration in `app/config.py` using Pydantic Settings, mapping the fields specified in the `CopyRepositoryRequest` API (e.g. `continue_on_skipped_version`, `max_version_age_days`, etc)
- [ ] Write failing test for `CopyRepository` API client in `tests/test_client.py` (Red Phase)
- [ ] Implement HTTP client utilizing Google Auth ADC in `app/client.py` (Green Phase)

## Phase 3: Application Server & Orchestration
- [ ] Write failing tests for FastAPI `/copy` endpoint in `tests/test_main.py`
- [ ] Implement FastAPI server orchestrating the multiple destination triggers in `app/main.py`
- [ ] Verify test coverage is >80% for backend codebase (`pytest --cov=app`)

## Phase 4: Containerization & Infrastructure
- [ ] Create a `Dockerfile` for the application
- [ ] Create Terraform configuration (`main.tf`, `variables.tf`) for deploying Cloud Run, Cloud Scheduler, and Artifact Registry (managing only the Cloud Run image AR repository).
- [ ] Draft robust Setup Instructions (`README.md`) detailing the fork-and-configure quick start process (under 10 minutes).
- [ ] Create `AGENTS.md` to ensure `README.md` and repository instructions stay automatically synced for AI agents.
