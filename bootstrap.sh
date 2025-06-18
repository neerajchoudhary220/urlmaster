#!/bin/bash

echo "📦 Setting up URL Master..."

# Step 1: Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Step 2: Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Install the CLI tool (inside the virtual env)
pip install .

# Step 4: Create a global symlink to make 'urlmaster' available globally
BIN_PATH="$(pwd)/.venv/bin/urlmaster"
LINK_PATH="/usr/local/bin/urlmaster"

if [ -L "$LINK_PATH" ] || [ -f "$LINK_PATH" ]; then
    echo "🔁 Removing existing global 'urlmaster' link..."
    sudo rm -f "$LINK_PATH"
fi

echo "🔗 Linking $BIN_PATH → $LINK_PATH"
sudo ln -s "$BIN_PATH" "$LINK_PATH"

echo "✅ URL Master installed globally!"
echo "👉 Now you can run: urlmaster serve"
