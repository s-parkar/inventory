# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose port (must match Flask port)
EXPOSE 5000

# Environment variables (Defaults, should be overridden by docker-compose or Jenkins)
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run gunicorn or python directly
CMD ["python", "run.py"]
