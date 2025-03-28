#FROM python:3.9 AS builder
#
#WORKDIR /app
#
#COPY requirements.txt .
#
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends \
#    bash git gcc musl-dev python3-dev swig libpq-dev build-essential netcat-openbsd supervisor vim cron net-tools telnet postgresql-client libqpdf-dev gdal-bin neovim zsh gfortran libopenblas-dev liblapack-dev && \
#    rm -rf /var/lib/apt/lists/*
#RUN python -m pip install --upgrade pip setuptools wheel && \
#    python -m pip install --no-cache-dir --default-timeout=100 -r requirements.txt
#
#FROM builder AS deployer
#WORKDIR /app
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#COPY . .

# Use official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN apt update
RUN apt install bash git gcc musl-dev python3-dev libpq-dev build-essential supervisor vim cron net-tools telnet postgresql-client gdal-bin neovim zsh -y \
     && python -m pip install --upgrade pip setuptools wheel
RUN pip install gunicorn && pip install uvicorn

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Expose the application port
#EXPOSE 8000

# Run the Django application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
