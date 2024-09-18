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
    git \
    && apt-get clean

# Upgrade pip to the latest version
RUN python3 -m pip install --upgrade pip 

# Set up a working directory
WORKDIR /app

# Clone the GarminConnectInterface repository
RUN git clone https://github.com/bshreyas13/GarminConnectInterface.git /app

# Install Garmin Connect package (garminconnect) and other requirements
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run in the container
CMD ["bash"]