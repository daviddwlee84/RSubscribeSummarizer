# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI application
# https://discuss.streamlit.io/t/streamlit-doesnt-reload-site-when-code-in-container-changes/46174
# set filWatcherType to pool if running Docker on Windows
CMD ["streamlit", "run", "./Overview.py", "--server.address", "0.0.0.0", "--server.port", "8001", "--server.headless", "true", "--server.fileWatcherType", "poll"]
