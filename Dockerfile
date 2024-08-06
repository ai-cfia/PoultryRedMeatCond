# Use the official Selenium base image with standalone Chrome
FROM selenium/standalone-chrome:latest

USER root

# Update the package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    python3 \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Create a virtual environment
RUN python3 -m venv /usr/src/app/venv

# Activate the virtual environment and upgrade pip
RUN /usr/src/app/venv/bin/pip install --upgrade pip

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install Python dependencies inside the virtual environment
RUN /usr/src/app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy your Selenium test scripts into the container
COPY . .

# Set the default command to run your Selenium Python script using the virtual environment's Python
CMD ["/usr/src/app/venv/bin/python", "-u", "CSV_downloader.py"]
