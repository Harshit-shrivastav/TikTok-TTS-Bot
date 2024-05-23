# Use the latest Python image from Docker Hub
FROM python:latest

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Set environment variables (if you have any, add them here)
ENV BOT_TOKEN = "TOKEN"

# Expose port 8000 to allow traffic on that port
EXPOSE 8000

# Run main.py when the container launches
CMD ["python", "main.py"]
