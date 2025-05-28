# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /usr/src/app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Default command
CMD ["python", "main.py"]
