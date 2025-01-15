# explain: # Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /api

# Copy application code
# COPY ./api ./


# Expose application port (if required)
EXPOSE 3000

# Start the application
CMD ["python", "api/main.py"]