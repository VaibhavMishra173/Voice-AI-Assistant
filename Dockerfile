# Use official slim Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Whisper separately
RUN pip install git+https://github.com/openai/whisper.git

# Copy the entire app
COPY . /app/

# Set PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH
