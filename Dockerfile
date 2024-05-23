# Use the latest Python image from Docker Hub
FROM python:latest

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Expose port 8000 to allow traffic on that port
EXPOSE 8000

# Run main.py with the virtual environment when the container launches
CMD ["sh", "-c", ". venv/bin/activate && python main.py"]
