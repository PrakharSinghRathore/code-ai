#!/bin/bash

echo "RCM Setup - Code Visualizer & Diagram Generator"
echo "=================================================="
echo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Backend setup
echo "Installing Backend Dependencies..."
cd "$SCRIPT_DIR/backend"
python -m pip install flask flask-cors python-dotenv requests

# Frontend setup
echo
echo "Installing Frontend Dependencies..."
cd "$SCRIPT_DIR/frontend"
python -m pip install streamlit requests

echo
echo "=================================================="
echo "Setup Complete!"
echo
echo "To run the project:"
echo "  ./run.sh"
echo
echo "Or manually:"
echo "  - Backend: cd backend && python app.py"
echo "  - Frontend: cd frontend && streamlit run app.py"
echo
