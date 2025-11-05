#!/bin/bash
#
# setup-dev.sh
#
# Development environment setup script for MeshView
# This script sets up the Python virtual environment and installs development tools

set -e

echo "Setting up MeshView development environment..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is not installed."
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "Creating Python virtual environment with uv..."
    uv venv env
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Install requirements
echo ""
echo "Installing requirements..."
uv pip install -r requirements.txt
echo "✓ Requirements installed"

# Install development tools
echo ""
echo "Installing development tools..."
uv pip install pre-commit pytest pytest-asyncio pytest-aiohttp
echo "✓ Development tools installed"

# Install pre-commit hooks
echo ""
echo "Installing pre-commit hooks..."
./env/bin/pre-commit install
echo "✓ Pre-commit hooks installed"

# Install graphviz check
echo ""
if command -v dot &> /dev/null; then
    echo "✓ graphviz is installed"
else
    echo "⚠ Warning: graphviz is not installed"
    echo "  Install it with:"
    echo "    macOS:   brew install graphviz"
    echo "    Debian:  sudo apt-get install graphviz"
fi

# Create config.ini if it doesn't exist
echo ""
if [ ! -f "config.ini" ]; then
    echo "Creating config.ini from sample..."
    cp sample.config.ini config.ini
    echo "✓ config.ini created"
    echo "  Edit config.ini to configure your MQTT and site settings"
else
    echo "✓ config.ini already exists"
fi

echo ""
echo "=========================================="
echo "Development environment setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit config.ini with your MQTT settings"
echo "  2. Run: ./env/bin/python mvrun.py"
echo "  3. Open: http://localhost:8081"
echo ""
echo "Pre-commit hooks are now active:"
echo "  - Ruff will auto-format and fix issues before each commit"
echo "  - If files are changed, you'll need to git add and commit again"
echo ""
echo "Run tests with: ./env/bin/pytest tests/"
echo ""
