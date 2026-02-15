#!/bin/bash
# Quick start script for ScribeMD

# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q anthropic flask

# Start the Flask server
echo "Starting ScribeMD on http://localhost:5001"
python app.py

