# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# In api directory
WORKDIR /app/api

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Back in app directory
WORKDIR /app

# Expose port
EXPOSE 80

# Launch with Uvicorn
CMD ["python", "main.py", "run-server"]