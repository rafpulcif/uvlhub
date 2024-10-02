# SCRIPT TO START FLASK PROJECT (DEVELOPMENT SERVER)

#!/bin/bash

PROJECT_DIR="/Users/rafapulido/VSCode/uvlhub"

cd $PROJECT_DIR

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "Virtual environment directory venv does not exist."
  exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if MariaDB is running
if ! pgrep -x "mysqld" > /dev/null; then
  sudo mysql.server start
else
  echo "MariaDB is already running."
fi

# Start Flask
flask run --host=0.0.0.0 --reload --debug

