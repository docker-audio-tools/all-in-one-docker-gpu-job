# Use a Python 3.8 base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y cmake build-essential

# Copy the requirements.txt file
#COPY requirements.txt .
COPY requirements_filtered.txt .

# Install torch, torchvision, torchaudio, and Cython first
RUN pip install --no-cache-dir torch torchvision torchaudio Cython

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements_filtered.txt
RUN pip install madmom==0.16.1
RUN pip install natten==0.15.0

# Copy the entire project to the /app directory
COPY . .

# Install the project in editable mode
RUN pip install -e .

# Set the entrypoint to run the allin1 command
ENTRYPOINT ["python", "-m", "allin1.cli"]
