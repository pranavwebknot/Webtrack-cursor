#!/bin/bash

# Exit on error
set -e

echo "Setting up WebTrack development environment..."

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install wheel
pip install --upgrade pip
pip install wheel setuptools

# Install requirements
pip install -r backend/requirements.txt

# Create necessary directories
mkdir -p backend/logs
mkdir -p backend/media
mkdir -p backend/static

# Create database
createdb webtrack

# Run migrations
cd backend
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Start the development server
echo "Starting development server..."
python manage.py runserver
