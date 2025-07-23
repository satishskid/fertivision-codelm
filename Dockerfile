# Dockerfile optimized for production deployment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads exports logs static/css static/js templates

# Set proper permissions
RUN chmod +x *.sh && \
    chown -R nobody:nogroup /app

# Switch to non-root user
USER nobody

# Health check with dynamic port
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Set environment variables for Cloud Run compatibility
ENV PORT=8080

# Expose port (Cloud Run will override this)
EXPOSE $PORT

# Default command with dynamic port binding
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 2 --worker-class gevent app:app
