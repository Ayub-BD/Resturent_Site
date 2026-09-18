#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python -m django collectstatic --no-input
python -m django migrate