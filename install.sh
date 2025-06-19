#!/bin/bash

echo "📦 Setting up URL Master..."

# --- Step 0: Check required global tools ---

# Check cloudflared
if command -v cloudflared &> /dev/null; then
    echo -e "\033[92m✅ 'cloudflared' is installed.\033[0m"
else
    echo -e "\033[91m❌ 'cloudflared' is not installed.\033[0m"
    echo -e "\033[93m👉 Please install it from: https://developers.cloudflare.com/cloudflared/\033[0m"
    exit 1
fi

# Check herd
if command -v herd &> /dev/null; then
    echo -e "\033[92m✅ 'herd' CLI is installed.\033[0m"
else
    echo -e "\033[91m❌ 'herd' CLI is not installed.\033[0m"
    echo -e "\033[93m👉 Please install it or ensure it's in your PATH.\033[0m"
    exit 1
fi

# --- Step 1: Create and activate virtual environment ---
python3 -m venv .venv
source .venv/bin/activate

# --- Step 2: Upgrade pip and install requirements ---
pip install --upgrade pip
pip install -r requirements.txt

# --- Step 3: Install the CLI tool (inside the virtual env) ---
pip install .

# --- Step 4: Create a global symlink ---
BIN_PATH="$(pwd)/.venv/bin/urlmaster"
LINK_PATH="/usr/local/bin/urlmaster"

if [ -L "$LINK_PATH" ] || [ -f "$LINK_PATH" ]; then
    echo "🔁 Removing existing global 'urlmaster' link..."
    sudo rm -f "$LINK_PATH"
fi

echo "🔗 Linking $BIN_PATH → $LINK_PATH"
sudo ln -s "$BIN_PATH" "$LINK_PATH"

echo -e "\033[92m✅ URL Master installed Successfully!\033[0m"

urlmaster