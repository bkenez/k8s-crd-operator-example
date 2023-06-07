# Use a Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python code into the container
COPY operator.py .

# Install the required dependencies
RUN pip install kubernetes

# Run the Python script
CMD ["python", "operator.py"]