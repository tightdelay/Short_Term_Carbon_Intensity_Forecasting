FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory to the working directory inside the container
COPY ./src /app/src

# Copy any additional files necessary (if any)

# Set the default command to execute the main calculation script
CMD ["python", "src/calculations.py"]