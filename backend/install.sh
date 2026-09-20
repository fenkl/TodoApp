#!/bin/bash

# Install script for TodoSync backend on Raspberry Pi
# This script sets up the environment for autonomous operation

echo "TodoSync Backend Installation Script for Raspberry Pi"
echo "====================================================="

# Check if running on Raspberry Pi
echo "Checking system architecture..."
if [[ $(uname -m) != "armv7l" && $(uname -m) != "aarch64" ]]; then
    echo "Warning: This script is intended for Raspberry Pi (ARM architecture)"
    read -p "Continue anyway? (y/n): " continue_anyway
    if [[ $continue_anyway != "y" ]]; then
        echo "Installation cancelled."
        exit 1
    fi
fi

# Update package list
echo ""
read -p "Update package list? (y/n): " update_pkgs
if [[ $update_pkgs == "y" ]]; then
    echo "Updating package list..."
    sudo apt update
    echo "Package list updated."
else
    echo "Skipping package list update."
fi

# Install Python 3 and pip
echo ""
read -p "Install Python 3 and pip? (y/n): " install_python
if [[ $install_python == "y" ]]; then
    echo "Installing Python 3 and pip..."
    sudo apt install -y python3 python3-pip
    echo "Python 3 and pip installed."
else
    echo "Skipping Python installation."
fi

# Install system dependencies
echo ""
read -p "Install system dependencies? (y/n): " install_deps
if [[ $install_deps == "y" ]]; then
    echo "Installing system dependencies..."
    sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
    echo "System dependencies installed."
else
    echo "Skipping system dependencies installation."
fi

# Create virtual environment
echo ""
read -p "Create Python virtual environment? (y/n): " create_venv
if [[ $create_venv == "y" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Skipping virtual environment creation."
fi

# Activate virtual environment and install Python packages
echo ""
read -p "Install Python dependencies? (y/n): " install_packages
if [[ $install_packages == "y" ]]; then
    echo "Activating virtual environment and installing packages..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Python dependencies installed."
else
    echo "Skipping Python package installation."
fi

# Create systemd service file for auto-startup
echo ""
read -p "Create systemd service for auto-startup? (y/n): " create_service
if [[ $create_service == "y" ]]; then
    echo "Creating systemd service..."
    
    # Read the current user for service file
    USER=$(whoami)
    echo "[Unit]
Description=TodoSync Backend Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/AndroidStudioProjects/TodoApp/backend
ExecStart=/home/$USER/AndroidStudioProjects/TodoApp/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target" > todosync-backend.service
    
    echo "Systemd service file created as todosync-backend.service"
    read -p "Install systemd service? (y/n): " install_service
    if [[ $install_service == "y" ]]; then
        sudo cp todosync-backend.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable todosync-backend.service
        echo "Systemd service installed and enabled."
    else
        echo "Service file created but not installed. You can install it manually with:"
        echo "sudo cp todosync-backend.service /etc/systemd/system/"
        echo "sudo systemctl daemon-reload"
        echo "sudo systemctl enable todosync-backend.service"
    fi
else
    echo "Skipping systemd service creation."
fi

# Create startup script
echo ""
read -p "Create startup script for auto-startup? (y/n): " create_startup
if [[ $create_startup == "y" ]]; then
    echo "Creating startup script..."
    
    echo "#!/bin/bash
# Startup script for TodoSync backend

# Change to the backend directory
cd /home/$(whoami)/AndroidStudioProjects/TodoApp/backend

# Activate virtual environment
source venv/bin/activate

# Start the FastAPI server with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000" > startup.sh
    
    chmod +x startup.sh
    echo "Startup script created as startup.sh"
else
    echo "Skipping startup script creation."
fi

# Create a database initialization script
echo ""
read -p "Create database initialization script? (y/n): " create_db_script
if [[ $create_db_script == "y" ]]; then
    echo "Creating database init script..."
    
    echo "#!/bin/bash
# Database initialization script for TodoSync backend

# Change to the backend directory
cd /home/$(whoami)/AndroidStudioProjects/TodoApp/backend

# Ensure virtual environment is activated and initialize the database
source venv/bin/activate
python3 -c \"from db import init_db; init_db()\"
echo \"Database initialized successfully\""
    
    chmod +x db_init.sh
    echo "Database initialization script created as db_init.sh"
else
    echo "Skipping database initialization script creation."
fi

# Create README for installation instructions
echo ""
read -p "Create installation documentation? (y/n): " create_docs
if [[ $create_docs == "y" ]]; then
    echo "Creating installation documentation..."
    
    echo "# TodoSync Backend Installation Guide

## Prerequisites

- Raspberry Pi with Raspbian OS (ARM architecture)
- Python 3.7 or higher
- Internet connection for package downloads

## Installation Steps

1. Make this script executable:
   \`\`\`bash
   chmod +x install.sh
   \`\`\`

2. Run the installation script:
   \`\`\`bash
   ./install.sh
   \`\`\`

3. When prompted, confirm each step of the installation process.

## Auto-start Configuration

To enable automatic startup on boot:

1. Enable the systemd service:
   \`\`\`bash
   sudo systemctl enable todosync-backend.service
   \`\`\`

2. Start the service immediately:
   \`\`\`bash
   sudo systemctl start todosync-backend.service
   \`\`\`

3. Check if the service is running:
   \`\`\`bash
   sudo systemctl status todosync-backend.service
   \`\`\`

## Manual Startup

To start the server manually:

1. Activate virtual environment:
   \`\`\`bash
   source venv/bin/activate
   \`\`\`

2. Start the server:
   \`\`\`bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   \`\`\`

## Service Management

To manage the service:
- Start: \`sudo systemctl start todosync-backend.service\`
- Stop: \`sudo systemctl stop todosync-backend.service\`
- Restart: \`sudo systemctl restart todosync-backend.service\`
- Check status: \`sudo systemctl status todosync-backend.service\`

## Troubleshooting

If you encounter any issues:

1. Check service logs:
   \`\`\`bash
   sudo journalctl -u todosync-backend.service
   \`\`\`

2. Verify Python dependencies are installed and correct:
   \`\`\`bash
   source venv/bin/activate && pip list
   \`\`\`

3. Run a manual database initialization:
   \`\`\`bash
   source venv/bin/activate && python3 -c \"from db import init_db; init_db()\"
   \`\`\`

## Security Notes

- The backend API is accessible from any IP address on port 8000 (default for FastAPI in development)
- In production, configure appropriate firewall rules
- Consider using HTTPS with a reverse proxy like Nginx
" > INSTALL.md
    
    echo "Installation documentation created as INSTALL.md"
else
    echo "Skipping documentation creation."
fi

echo ""
echo "Installation completed!"
echo ""
echo "To start the service manually:"
echo "  sudo systemctl start todosync-backend.service"
echo ""
echo "To check the service status:"
echo "  sudo systemctl status todosync-backend.service"
echo ""
echo "To enable auto-start on boot:"
echo "  sudo systemctl enable todosync-backend.service"