FROM python:3.13-slim

WORKDIR /app

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Copying pyproject.toml and uv.lock first for caching layers
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose port for Cloud Run
EXPOSE 8080

# Command to run uvicorn on port 8080 (Cloud Run expected port)
CMD ["uv", "run", "python", "main.py"]
