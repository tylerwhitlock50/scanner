#!/bin/bash

# Navigate to the backend directory
cd ~/scanner/backend

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/Scripts/activate  # for Linux or MacOS use: source venv/bin/activate
echo "Virtual environment activated."

# Install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed."
else
    echo "requirements.txt not found!"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    touch .env
    echo ".env file created."
    # You can also add some initial content to the .env file like this:
    # echo "API_KEY=your_api_key_here" > .env
else
    echo ".env file already exists."
fi

# Create service-account-file.json file if it doesn't exist
if [ ! -f "service-account-file.json" ]; then
    touch service-account-file.json
    echo "service-account-file.json file created."
else
    echo "service-account-file.json already exists."
fi
echo "Please add your service account file to the service-account-file.json file."
echo "Setup completed!"
