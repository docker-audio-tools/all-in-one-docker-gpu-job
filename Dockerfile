# Use a Python 3.8 base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the /app directory
COPY . .

# Install the project in editable mode
RUN pip install -e .

# Set the entrypoint to run the allin1 command
ENTRYPOINT ["python", "-m", "allin1.cli"]
