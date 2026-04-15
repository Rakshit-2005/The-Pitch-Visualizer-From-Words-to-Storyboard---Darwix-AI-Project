#!/bin/bash

# Pitch Visualizer - Setup Script for Mac/Linux

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   Pitch Visualizer - Setup Script     ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check Python
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+ from https://python.org"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
echo ""
echo "[2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "[3/4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"

# Install requirements
echo ""
echo "[4/4] Installing dependencies (this may take 5-10 minutes)..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "═══════════════════════════════════════"
echo "✨ Setup complete!"
echo "═══════════════════════════════════════"
echo ""
echo "To start the app, run:"
echo "  python app.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
