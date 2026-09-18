#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files & Run migrations
python manage.py collectstatic --no-input --settings=config.settings
python manage.py migrate --settings=config.settings
