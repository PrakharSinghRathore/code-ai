#!/bin/bash

# RCM - Start both backend and frontend

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting RCM Backend..."
cd "$SCRIPT_DIR/backend"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi
source venv/bin/activate
python app.py &
BACKEND_PID=$!

sleep 2

echo "Starting RCM Frontend..."
cd "$SCRIPT_DIR/frontend"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi
source venv/bin/activate
streamlit run app.py

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT
