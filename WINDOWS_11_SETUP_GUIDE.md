# Windows 11 Setup Guide for PyMapGIS Jupyter Environment

This guide provides step-by-step instructions for Windows 11 users to set up and run the PyMapGIS Jupyter environment using WSL 2, Docker, and Docker Desktop.

## Prerequisites

- Windows 11 (Home, Pro, or Enterprise)
- Administrator privileges
- At least 8GB RAM (16GB recommended)
- At least 20GB free disk space

## Step 1: Enable WSL 2

### 1.1 Enable Windows Subsystem for Linux
Open PowerShell as Administrator and run:

```powershell
# Enable WSL and Virtual Machine Platform
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart your computer
Restart-Computer
```

### 1.2 Set WSL 2 as Default
After restart, open PowerShell as Administrator:

```powershell
# Set WSL 2 as default version
wsl --set-default-version 2

# Install Ubuntu (recommended distribution)
wsl --install -d Ubuntu
```

### 1.3 Complete Ubuntu Setup
1. After installation, Ubuntu will launch automatically
2. Create a username and password when prompted
3. Update the system:

```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install Docker Desktop

### 2.1 Download and Install
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
2. Run the installer with default settings
3. **Important**: Ensure "Use WSL 2 instead of Hyper-V" is checked during installation
4. Restart your computer when prompted

### 2.2 Configure Docker Desktop
1. Launch Docker Desktop
2. Go to Settings → General
3. Ensure "Use the WSL 2 based engine" is checked
4. Go to Settings → Resources → WSL Integration
5. Enable integration with your Ubuntu distribution
6. Click "Apply & Restart"

## Step 3: Verify Installation

### 3.1 Test WSL 2
Open Ubuntu from Start Menu and run:

```bash
# Check WSL version
wsl -l -v

# Should show Ubuntu with version 2
```

### 3.2 Test Docker in WSL
In your Ubuntu terminal:

```bash
# Test Docker installation
docker --version
docker run hello-world
```

## Step 4: Run PyMapGIS Jupyter Environment

### 4.1 Quick Start (Recommended)
In your Ubuntu terminal:

```bash
# Pull and run the secure PyMapGIS Jupyter environment
docker pull nicholaskarlson/pymapgis-jupyter:secure
docker run -d -p 8888:8888 --name pymapgis-jupyter nicholaskarlson/pymapgis-jupyter:secure
```

### 4.2 Access the Environment
1. Open your web browser (Chrome, Edge, or Firefox)
2. Navigate to: http://localhost:8888
3. The Jupyter Lab interface will load automatically (no token required)

### 4.3 Run the Modesto Example
1. In Jupyter Lab, navigate to the `notebooks` folder
2. Open `modesto_spatial_dbscan.ipynb`
3. Run all cells by clicking "Run" → "Run All Cells"
4. The interactive map will appear at the bottom of the notebook

## Step 5: Alternative Setup Methods

### 5.1 Clone and Build Locally
If you want to modify the environment:

```bash
# Install Git in Ubuntu
sudo apt install git -y

# Clone the repository
git clone https://github.com/nicholaskarlson/pymapgis-jupyter.git
cd pymapgis-jupyter

# Build the Docker image
docker build -t pymapgis-jupyter .

# Run the container
docker run -d -p 8888:8888 --name pymapgis-jupyter pymapgis-jupyter
```

### 5.2 Using Docker Compose
For development with volume mounting:

```bash
# In the cloned repository directory
docker-compose up -d

# This will mount the notebooks directory for live editing
```

## Step 6: Managing the Environment

### 6.1 Container Management
```bash
# Stop the container
docker stop pymapgis-jupyter

# Start the container
docker start pymapgis-jupyter

# Remove the container
docker rm pymapgis-jupyter

# View running containers
docker ps
```

### 6.2 Accessing Container Shell
```bash
# Access the container's bash shell
docker exec -it pymapgis-jupyter bash
```

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: WSL 2 Installation Fails
**Solution**: Ensure virtualization is enabled in BIOS/UEFI settings

#### Issue 2: Docker Desktop Won't Start
**Solutions**:
- Restart Docker Desktop as Administrator
- Check Windows Features: Hyper-V should be disabled if using WSL 2
- Ensure WSL 2 is properly installed

#### Issue 3: Cannot Access http://localhost:8888
**Solutions**:
- Check if container is running: `docker ps`
- Verify port mapping: `docker port pymapgis-jupyter`
- Try http://127.0.0.1:8888 instead

#### Issue 4: Jupyter Notebook Kernel Issues
**Solutions**:
- Restart the container: `docker restart pymapgis-jupyter`
- Check container logs: `docker logs pymapgis-jupyter`

#### Issue 5: Performance Issues
**Solutions**:
- Allocate more resources to Docker Desktop (Settings → Resources)
- Close unnecessary applications
- Ensure at least 4GB RAM allocated to Docker

### Getting Help

1. **Docker Desktop Issues**: Check Docker Desktop documentation
2. **WSL 2 Issues**: Visit Microsoft WSL documentation
3. **PyMapGIS Issues**: Check the main PyMapGIS documentation
4. **Repository Issues**: Open an issue on GitHub

## Performance Tips

1. **Resource Allocation**: Allocate at least 4GB RAM to Docker Desktop
2. **Storage**: Use Docker Desktop's disk cleanup feature regularly
3. **WSL 2**: Keep Ubuntu updated with `sudo apt update && sudo apt upgrade`
4. **Windows**: Ensure Windows 11 is up to date

## Security Considerations

- The container runs with minimal privileges
- No external network access required for basic functionality
- All data processing happens locally
- See SECURITY.md for detailed security information

## Next Steps

After successfully running the Modesto example:

1. Explore other notebooks in the `notebooks/` directory
2. Modify the Modesto example for your own geographic area
3. Create new spatial analysis notebooks
4. Contribute improvements back to the repository

## Additional Resources

- [Docker Desktop for Windows Documentation](https://docs.docker.com/desktop/windows/)
- [WSL 2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [PyMapGIS on PyPI](https://pypi.org/project/pymapgis/) - Main PyMapGIS library and installation
- [Jupyter Lab Documentation](https://jupyterlab.readthedocs.io/)
