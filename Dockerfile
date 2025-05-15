# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies with increased pip timeout
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set environment variable (optional)
ENV PYTHONUNBUFFERED=1

# Command to run your app (adjust as needed)
CMD ["python", "app.py"]
