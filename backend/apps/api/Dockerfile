FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast python package management
RUN pip install --no-cache-dir uv

# Copy shared packages and api app
COPY apps/packages /app/apps/packages
COPY apps/api /app/apps/api

WORKDIR /app/apps/api

# Install dependencies in system python
RUN uv pip install --system -e .

EXPOSE 8000

CMD ["python", "main.py"]
