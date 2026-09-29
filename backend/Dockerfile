FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .

# Expose port Flask API
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
