# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# # Tests
# RUN python -m pytest tests/unit -v

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Start the Flask application
#CMD ["python", "-m", "uvicorn", "main:app", "--reload"]
CMD ["python", "main.py"]