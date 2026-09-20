# TodoSync Deployment Guide

## Overview

This document provides comprehensive instructions for deploying the TodoSync application across different environments. The application supports cross-platform deployment with Tauri 2.0, including Linux, Windows, macOS, and Android.

## Prerequisites

Before deployment, ensure you have:

### Development Environment
- Node.js (v16 or higher) and npm
- Rust toolchain (latest stable version)
- Git for version control
- Android development tools (for Android builds)

### Production Environment
- Raspberry Pi with Raspbian OS (ARM architecture) for backend server
- Docker engine (optional, for containerized deployment)
- SSL certificates (for production HTTPS)

## Backend Deployment

### Raspberry Pi Setup

The TodoSync backend is designed to run autonomously on a Raspberry Pi:

1. **Initial Setup:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd TodoApp
   
   # Make the installation script executable
   chmod +x backend/install.sh
   
   # Run the installation script
   ./backend/install.sh
   ```

2. **Manual Installation Steps** (if not using installer):
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3 python3-pip build-essential libssl-dev libffi-dev python3-dev
   
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   
   # Install Python packages
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Initialize database
   python3 -c "from backend.db import init_db; init_db()"
   ```

3. **Service Configuration:**
   ```bash
   # Enable auto-start on boot
   sudo systemctl enable todosync-backend.service
   
   # Start the service
   sudo systemctl start todosync-backend.service
   
   # Check status
   sudo systemctl status todosync-backend.service
   ```

### Docker Deployment (Optional)

For container-based deployment:

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY backend/ ./backend/
   COPY src/ ./src/
   
   EXPOSE 8000
   CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and Run:**
   ```bash
   docker build -t todosync-backend .
   docker run -d -p 8000:8000 --name todosync-backend todosync-backend
   ```

## Frontend Deployment

### Web Application Build

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Build for production:**
   ```bash
   npm run build
   ```

3. **Serve the application:**
   The built files in `dist/` directory can be served by any web server.

### Desktop Application Build

1. **Build for different platforms:**
   ```bash
   # For Linux (AppImage)
   npm run tauri build --target linux
   
   # For Windows
   npm run tauri build --target windows
   
   # For macOS
   npm run tauri build --target macos
   ```

### Android Application Build

1. **Build the APK:**
   ```bash
   # Make build script executable
   chmod +x build.sh
   
   # Run the build script
   ./build.sh
   ```

2. **Install on device:**
   ```bash
   # Connect Android device with ADB enabled
   npm run tauri android dev
   # or for release build:
   npm run tauri android build --release
   ```

## Network Configuration

### Backend Server Setup

1. **Configure Firewall (if needed):**
   ```bash
   sudo ufw allow 8000/tcp
   ```

2. **Access from other devices:**
   Ensure the backend is accessible on the local network at `http://<pi-ip>:8000`

3. **Environment Variables (optional):**
   Create a `.env` file in the backend directory:
   ```env
   BACKEND_PORT=8000
   DATABASE_URL=sqlite:///todos.db
   ```

## Testing Deployment

### Backend Verification
```bash  
# Test API endpoints
curl http://localhost:8000/api/v1/todos

# Check database initialization
python3 -c "from backend.db import get_db; print('Database connected successfully')"
```

### Frontend Verification
1. **Start development server:**
   ```bash
   npm run dev
   ```

2. **Connect to backend API:**
   Ensure frontend can connect to the backend at `http://192.168.2.2:8000`

3. **Test synchronization:**
   - Launch the application
   - Perform todo operations
   - Verify real-time updates across connected clients

## Production Deployment Checklist

### Before Starting:
- [ ] Backend server is accessible on LAN (port 8000)
- [ ] Device has sufficient storage for SQLite database  
- [ ] Network connectivity between devices
- [ ] Appropriate permissions for file system access
- [ ] Secure network configuration if deployed outside local network

### Installation Steps:
1. [ ] Run backend installation script or manual setup
2. [ ] Verify database initialization 
3. [ ] Start backend service
4. [ ] Test API connectivity from client devices
5. [ ] Configure client applications to connect to backend server
6. [ ] Deploy client applications on target devices
7. [ ] Verify offline queue and sync functionality

### Security Considerations:
1. [ ] Ensure proper firewall rules are enforced
2. [ ] Implement secure access to backend database
3. [ ] Review and update application permissions for mobile devices
4. [ ] Test network security in the deployment environment  

## Monitoring and Maintenance

### Backend Logs
```bash
# Check service logs
sudo journalctl -u todosync-backend.service -f

# Check system logs
sudo dmesg | grep -i todo
```

### Database Management
```bash
# Connect to database for maintenance (if needed)
sqlite3 backend/todos.db
```

### Service Management
```bash
# Start service
sudo systemctl start todosync-backend.service

# Stop service  
sudo systemctl stop todosync-backend.service

# Restart service
sudo systemctl restart todosync-backend.service

# Check status  
sudo systemctl status todosync-backend.service
```

## Troubleshooting

### Common Issues:

| Issue | Solution |
|-------|----------|
| API not responding | Verify backend is running: `sudo systemctl status todosync-backend.service` |
| Database connection error | Check database initialization and permissions |
| WebSocket connection fails | Ensure network connectivity between clients and server |
| Mobile app crashes on startup | Verify Android SDK tools are properly installed |
| Offline sync issues | Check localStorage persistence in frontend |

### Network Troubleshooting:
```bash
# Test connectivity to backend
ping 192.168.2.2
telnet 192.168.2.2 8000

# Check if port is open
nmap -p 8000 192.168.2.2
```

## Support and Updates

### Regular Maintenance:
- Monitor service status regularly
- Back up database files periodically  
- Update application components as needed
- Review security patches for dependencies

### Update Process:
1. Pull latest code from repository: `git pull origin main`
2. Rebuild backend components if applicable
3. Update client applications
4. Restart services:
   ```bash
   sudo systemctl restart todosync-backend.service
   ```

## License and Compliance

This deployment guide is part of the TodoSync project and follows the MIT license for the underlying source code.