# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file initially to take advantage of Docker's layer caching
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the entire container
COPY . /app

# Export port 5000 (optional, in case you use Flask or other servers in the future)
EXPOSE 5000

# Set the entry point to run the main.py file
CMD ["python", "main.py"]

#FROM ubuntu:latest
#LABEL authors="irfan"

#ENTRYPOINT ["top", "-b"]