#!/bin/bash

cd /var/www/html

echo "Updating website..."
git pull origin main

echo "Running site scripts..."
# example if you want your python scripts to run automatically
# python3 your_script.py

echo "Deployment complete."
