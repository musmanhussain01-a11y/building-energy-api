#!/bin/bash

# Setup script for Building Energy Data API
# Usage: bash setup.sh

echo "🚀 Setting up Building Energy Data API..."
echo ""

# Check Python version
python3 --version 2>/dev/null
if [ $? -ne 0 ]; then
    python --version
fi

echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv 2>/dev/null || python -m venv venv
echo "✅ Virtual environment created"

echo ""
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✅ Virtual environment activated"

echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "✨ Setup complete!"
echo ""
echo "To run the API:"
echo "  python main.py"
echo ""
echo "To run tests:"
echo "  pytest test_main.py -v"
echo ""
echo "To run example usage:"
echo "  python example_usage.py"
echo ""
echo "View API docs at:"
echo "  http://localhost:8000/docs"
