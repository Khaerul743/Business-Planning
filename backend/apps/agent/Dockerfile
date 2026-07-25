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

# Copy shared packages and agent app
COPY apps/packages /app/apps/packages
COPY apps/agent /app/apps/agent

WORKDIR /app/apps/agent

# Install dependencies in system python
RUN uv pip install --system -e .

EXPOSE 2024

CMD ["python", "main.py"]
