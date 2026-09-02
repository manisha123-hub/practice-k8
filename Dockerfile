# Use Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY app.py .

# Flask runs on port 5000
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
