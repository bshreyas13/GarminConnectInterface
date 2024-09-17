# Use an official Ubuntu as a base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install required dependencies
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean

# Upgrade pip to the latest version
RUN python3 -m pip install --upgrade pip

# Install Garmin Connect package (garminconnect)
RUN pip install --no-cache-dir -r requirements.txt

# Set up a working directory
WORKDIR /app

# Copy local files to the container's working directory (if needed)
COPY . /app

# Default command to run in the container
CMD ["bash"]

