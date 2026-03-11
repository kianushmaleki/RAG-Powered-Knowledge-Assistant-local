# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements (if exists) and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy project files
COPY . .

# Expose port (if needed for future API)
EXPOSE 8080

# Default command: run main.py
CMD ["python", "main.py"]
