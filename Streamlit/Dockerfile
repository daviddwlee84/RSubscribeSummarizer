# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI application
CMD ["streamlit", "run", "./Overview.py", "--server.address", "0.0.0.0", "--server.port", "8001", "--server.headless", "true"]
