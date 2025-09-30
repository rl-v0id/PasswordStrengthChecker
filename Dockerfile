# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


# Install system dependencies (add curl for healthcheck)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Health check (robust: try both new and old endpoints)
HEALTHCHECK CMD curl --fail http://localhost:8501/healthz || curl --fail http://localhost:8501/_stcore/health || exit 1

# Create non-root user for security, fix permissions
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app

# Switch to non-root user only after all files are owned
USER appuser

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none"]