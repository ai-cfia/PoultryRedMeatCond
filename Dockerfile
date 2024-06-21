# Use the official Selenium base image with standalone Chrome
FROM selenium/standalone-chrome:latest

USER root

# Update the package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

ARG NEW_REPORT_URL
ENV NEW_REPORT_URL=$NEW_REPORT_URL
ARG MASTERLIST_URL
ENV MASTERLIST_URL=$MASTERLIST_URL

# Copy the requirements.txt file into the container
COPY requirements.txt ./

COPY . /usr/src/app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your Selenium test scripts into the container
COPY . .

# Replace `your_script.py` with the name of your Selenium Python script
CMD ["python3", "-u", "CSV_downloader.py"]
