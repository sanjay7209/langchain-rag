# --------------------------------------------------------------------
# Stage 1: Build and install dependencies
# --------------------------------------------------------------------
FROM python:3.13-slim AS builder

# Set working directory
WORKDIR /usr/local/app

# System dependencies (add more if your Python libs require them)
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first for better build caching
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt

# --------------------------------------------------------------------
# Stage 2: Runtime image 
# --------------------------------------------------------------------
FROM python:3.13-slim

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/install/bin:$PATH"

WORKDIR /usr/local/app

# Copy only installed packages from builder
COPY --from=builder /install /usr/local

# Copy source code
COPY src ./src

# Optional: ensure logs & data directories exist
RUN mkdir -p /usr/local/app/logs

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Expose app port
EXPOSE 8080

# Default command to start the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
