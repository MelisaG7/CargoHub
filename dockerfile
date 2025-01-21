# explain: # Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /api

# Copy application code
# COPY ./api ./

# Install Python dependencies directly and run safety check after installing dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools==75.8.0 && \
    pip install --no-cache-dir fastapi uvicorn pytest flake8 pytest-cov safety && \
    safety check --full-report   

# Expose application port (if required)
EXPOSE 3000

# Start the application
CMD ["python", "api/main.py"]