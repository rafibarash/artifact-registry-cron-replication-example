FROM python:3.13-slim

WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for Cloud Run
EXPOSE 8080

# Command to run uvicorn on port 8080 (Cloud Run expected port)
CMD ["python", "main.py"]
