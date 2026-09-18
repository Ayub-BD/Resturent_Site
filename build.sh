#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input --settings=config.settings
python manage.py migrate --settings=config.settings