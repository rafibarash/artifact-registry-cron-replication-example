# Technology Stack: Artifact Registry Cron Replicator

## 1. Core Application
*   **Language:** Python 3.13+
*   **Framework:** FastAPI (for the lightweight web server)
*   **Asynchronous:** Uvicorn (ASGI server for FastAPI)

## 2. Google Cloud Platform Services
*   **Compute:** Cloud Run (Serverless container execution for the replication job)
*   **Orchestration/Scheduling:** Cloud Scheduler (For cron-based triggering of the Cloud Run job)
*   **Container Registry:** Artifact Registry (To host the Cloud Run job's Docker image, and the source/destination for replication)
*   **API Interaction:** Direct HTTP calls to the experimental `CopyRepository` API endpoint within Artifact Registry. Optionally, `GetOperation` calls will be made for polling if enabled via an environment flag.
*   **Authentication:** Google Application Default Credentials (ADC) via service accounts for Cloud Run

## 3. Development & Operations
*   **Version Control:** Git / GitHub (For hosting the forkable repository)
*   **Containerization:** Docker (For building the Cloud Run job image)
*   **Infrastructure as Code:** Terraform (For provisioning GCP resources like Cloud Run, Cloud Scheduler, and Artifact Registry repositories.)
*   **Python Package Management:** uv (For dependency management and environment creation during local development)

## 4. Key Libraries (Python)
*   `fastapi`: Web framework
*   `uvicorn`: ASGI server
*   `google-auth`: Google Authentication Library
*   `pydantic`: Data validation and settings management (used by FastAPI)
*   `httpx`: For making direct HTTP API calls
*   `uv`: Python package and environment manager

## 5. Justification
This stack is chosen for its alignment with the project goals of simplicity, ease of deployment on Google Cloud, and direct interaction with the experimental Artifact Registry API. Python with FastAPI provides a lightweight and efficient server for the Cloud Run environment, while Google Cloud services offer native integration and scalability. Terraform provides a robust and widely-adopted solution for Infrastructure as Code. Using `uv` streamlines local Python development.