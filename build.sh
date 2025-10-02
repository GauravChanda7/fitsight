#!/usr/bin/env bash
# exit on error
set -o errexit

# Install all the packages from requirements.txt
pip install -r requirements.txt

# Run Django's collectstatic command to gather all static files
python manage.py collectstatic --no-input

# Apply any new database migrations
python manage.py migrate