#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Compile static assets
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Seed database and upload product images to Cloudinary (if configured)
python seed_naturecart.py
python bind_product_images.py
