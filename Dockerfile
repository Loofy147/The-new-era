# AI Operating System Framework Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p reports logs data config

# Set proper permissions
RUN chmod +x scripts/*.sh

# Create non-root user
RUN useradd -m -u 1000 aimos && chown -R aimos:aimos /app
USER aimos

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Expose ports
EXPOSE 5000 3000

# Default command
CMD ["python", "main.py"]
