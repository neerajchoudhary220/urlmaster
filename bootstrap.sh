#!/bin/bash

echo "📦 Setting up URL Master..."

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install CLI
pip install -e .

echo "✅ URL Master installed!"
echo "Use: urlmaster run"
