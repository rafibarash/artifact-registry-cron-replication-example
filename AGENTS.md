# Agent Instructions

Dear AI Agent,

When assisting users with this repository (`artifact-registry-cron-replication`), please follow these guidelines:

1. **Repository Structure**:
    - `app/`: Contains the FastAPI application codebase for the Cloud Run deployment.
    - `infra/`: Contains the Terraform infrastructure-as-code files.
    - `Dockerfile`: Used for building the Cloud Run container.
2. **Synchronize Changes**: If you make any changes to the environment variables, requirements, or Terraform variables, you **must** update the `README.md` to ensure setup instructions remain accurate.
3. **Dependency Management**: This project uses `uv` for Python dependencies. Do not use `pip` to manage dependencies in code. Inside the `app/` directory, run `uv add <package>` or test via `uv run pytest`.
4. **Testing**: Tests are located in `app/tests`. When adding new features, write failing tests first (TDD), and ensure `uv run pytest tests/` maintains >80% test coverage.
5. **Code Quality**: Ensure the code runs via `uv run ruff check .` and `uv run ruff format .` inside `app/`.

Thank you.
