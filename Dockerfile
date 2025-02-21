# Use the official Python image
FROM python:3.13

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app/

RUN useradd -m vscode && \
    echo 'vscode:123456' | chpasswd && \
    adduser vscode sudo

USER vscode

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for Django
EXPOSE 8000
