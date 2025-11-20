# Use official Python image as base
FROM python:3.12.12-slim

# Set working directory
WORKDIR /app/back

# Copy only dependency files first for better caching
COPY back/requirements.txt ./

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy project files
COPY back/. .

# Expose port (if your app uses a specific port, adjust accordingly)
EXPOSE 8000

# Default command (adjust if your entry point is different)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["fastapi", "run"]

