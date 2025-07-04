# Running Modesto Spatial DBSCAN with Secure Docker Image

## 🐳 Quick Start with Secure Docker Image

### 1. Pull the Latest Secure Image
```bash
# Pull the security-hardened image
docker pull nicholaskarlson/pymapgis-jupyter:secure
```

### 2. Run the Secure Container
```bash
# Basic secure deployment
docker run -d \
  --name modesto-analysis \
  -p 8888:8888 \
  nicholaskarlson/pymapgis-jupyter:secure
```

### 3. Access Jupyter Lab
Open your browser and navigate to:
```
http://localhost:8888
```

### 4. Open the Modesto Analysis Notebook
Navigate to: `notebooks/modesto_spatial_dbscan.ipynb`

## 🔒 Enhanced Security Deployment

For production or sensitive environments, use these additional security measures:

```bash
# Maximum security deployment
docker run -d \
  --name modesto-analysis-secure \
  --user 1000:1000 \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /home/jupyter/.local \
  --tmpfs /home/jupyter/.cache \
  --security-opt no-new-privileges:true \
  --cap-drop ALL \
  --cap-add CHOWN \
  --cap-add SETUID \
  --cap-add SETGID \
  -p 8888:8888 \
  -v $(pwd)/notebooks:/home/jupyter/notebooks:ro \
  nicholaskarlson/pymapgis-jupyter:secure
```

## 📊 Code Changes for Modesto, California

### Key Updates Made:

1. **Location Change**: From Little Rock, Arkansas to Modesto, California
2. **Coordinate Updates**: 
   - Downtown Modesto: `37.6391°N, 121.0018°W` (10th & I Street area)
   - Vintage Faire Mall: `37.6764°N, 121.0244°W` (North Modesto)
3. **Projection System**: UTM Zone 10N (EPSG:26910) for Central California
4. **Regional Bounds**: Stanislaus County boundaries for noise generation
5. **Docker Integration**: Removed pip install commands (pre-installed packages)

### Original vs Updated Code:

#### Hotspot Locations
```python
# BEFORE (Little Rock, Arkansas)
downtown = [
    Point(np.random.normal(-92.2896, 0.002),   # lon
          np.random.normal(34.7465, 0.002))    # lat
    for _ in range(50)
]

# AFTER (Modesto, California)
downtown_modesto = [
    Point(np.random.normal(-121.0018, 0.002),   # lon
          np.random.normal(37.6391, 0.002))     # lat
    for _ in range(50)
]
```

#### Projection System
```python
# BEFORE (Arkansas)
incidents_m = incidents_gdf.to_crs(epsg=26952)  # Arkansas South NAD83

# AFTER (California)
incidents_m = incidents_gdf.to_crs(epsg=26910)  # UTM Zone 10N
```

## 🗺️ Geographic Context

### Modesto, California Details:
- **County**: Stanislaus County
- **Population**: ~218,000 (2020 census)
- **Location**: Central Valley, California
- **Coordinates**: 37.6391°N, 121.0018°W
- **UTM Zone**: 10N (EPSG:26910)

### Analysis Areas:
1. **Downtown Modesto**: Historic city center, business district
2. **Vintage Faire Mall**: Major shopping area, North Modesto
3. **Regional Noise**: Scattered across Stanislaus County

## 🚀 Running the Analysis

### Step-by-Step Execution:

1. **Start the Container**:
   ```bash
   docker run -d --name modesto-analysis -p 8888:8888 nicholaskarlson/pymapgis-jupyter:secure
   ```

2. **Access Jupyter Lab**:
   - Open browser: `http://localhost:8888`
   - No token required (configured for development)

3. **Run the Notebook**:
   - Navigate to `notebooks/modesto_spatial_dbscan.ipynb`
   - Execute cells sequentially (Shift + Enter)

4. **View Results**:
   - Interactive map shows clusters in Modesto
   - Cluster statistics printed in output
   - Noise points identified

### Expected Output:
```
✅ Generated 130 simulated incidents in Modesto area.
✅ Reprojected to UTM Zone 10N for accurate distance calculations.

🚀 Running Spatial DBSCAN…
   ✅ DBSCAN complete.

--- Cluster counts ---
-1    40  # Noise points
 0    50  # Downtown cluster
 1    40  # Vintage Faire cluster
----------------------

🎨 Building interactive map of Modesto…
🎉 Map ready! (Cluster −1 = noise)
📍 Map centered on Downtown Modesto, California
```

## 🔧 Troubleshooting

### Common Issues:

1. **Port Already in Use**:
   ```bash
   # Check what's using port 8888
   docker ps
   # Stop existing container
   docker stop <container_name>
   ```

2. **Permission Issues**:
   ```bash
   # Ensure proper user permissions
   docker run --user 1000:1000 ...
   ```

3. **Memory Issues**:
   ```bash
   # Increase memory limit
   docker run --memory=2g ...
   ```

### Container Management:

```bash
# View running containers
docker ps

# View logs
docker logs modesto-analysis

# Stop container
docker stop modesto-analysis

# Remove container
docker rm modesto-analysis

# Clean up
docker system prune
```

## 📈 Performance Optimization

### For Large Datasets:
```bash
# Increase memory and CPU limits
docker run -d \
  --name modesto-analysis-optimized \
  --memory=4g \
  --cpus=2 \
  -p 8888:8888 \
  nicholaskarlson/pymapgis-jupyter:secure
```

### For Persistent Storage:
```bash
# Mount local directory for data persistence
docker run -d \
  --name modesto-analysis-persistent \
  -p 8888:8888 \
  -v $(pwd)/data:/home/jupyter/data \
  -v $(pwd)/notebooks:/home/jupyter/notebooks \
  nicholaskarlson/pymapgis-jupyter:secure
```

## ✅ Security Verification

Verify the container is running securely:

```bash
# Check user (should be 'jupyter', not 'root')
docker exec modesto-analysis whoami

# Check security settings
docker inspect modesto-analysis | grep -A 10 "SecurityOpt"

# Verify PyMapGIS installation
docker exec modesto-analysis python -c "import pymapgis; print('✅ PyMapGIS ready')"
```

The secure Docker environment provides a production-ready platform for spatial analysis with enterprise-grade security!
