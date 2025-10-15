# Use a Python 3.8 base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y cmake build-essential
RUN pip install --upgrade pip

# Copy the requirements.txt file
#COPY requirements.txt .
COPY requirements_filtered.txt .

# Install torch, torchvision, torchaudio, and Cython first
# Torch 2.2.2 CPU (no CUDA)
RUN pip install --no-cache-dir torch==2.2.2 torchvision torchaudio==2.2.2 cython

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements_filtered.txt
RUN pip install madmom==0.16.1

# CPU only version
RUN pip install natten==0.15.0

# Copy the entire project to the /app directory
COPY . .

# Install the project in editable mode
RUN pip install -e .

# WARNING each execution downloads the demucs model again
# Downloading: "https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/955717e8-8726e21a.th" to /root/.cache/torch/hub/checkpoints/955717e8-8726e21a.th

# Set the entrypoint to run the allin1 command
ENTRYPOINT ["python", "-m", "allin1.cli"]
