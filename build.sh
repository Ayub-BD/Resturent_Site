#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# manage.py ফাইলটি যে ফোল্ডারে আছে সেখানে যাওয়ার জন্য নিচের লাইনটি ঠিক করুন (যদি restaurant_project ফোল্ডারের ভেতরে থাকে)
cd restaurant_project

# Collect static files & Run migrations
python manage.py collectstatic --no-input --settings=config.settings
python manage.py migrate --settings=config.settings
