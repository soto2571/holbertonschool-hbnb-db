# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src
ENV FLASK_ENV=production

# Install dependencies
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    build-base \
    linux-headers

# Set work directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy .env file
COPY .env /app/.env

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src:app"]