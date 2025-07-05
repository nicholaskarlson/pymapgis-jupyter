# 🚀 Quick Start Guide

Get up and running with PyMapGIS Jupyter in minutes! This guide will have you creating spatial analysis notebooks for your own city in no time.

## ⚡ 5-Minute Setup

### Step 1: Start the Environment
```bash
# Pull and run the PyMapGIS Jupyter container
docker pull nicholaskarlson/pymapgis-jupyter:secure
docker run -d -p 8888:8888 --name pymapgis-jupyter nicholaskarlson/pymapgis-jupyter:secure
```

### Step 2: Access Jupyter Lab
1. Open your browser
2. Navigate to `http://localhost:8888`
3. Jupyter Lab will load automatically (no token required)

### Step 3: Try an Example
1. Navigate to the `notebooks/` folder
2. Open `getting_started.ipynb`
3. Run all cells (Shift + Enter for each cell)

## 🏙️ Create Your First City Analysis

### Option A: Use a Template (Recommended)
1. **Choose your city size:**
   - Small city (50k-200k): Use Modesto template
   - Medium city (200k-500k): Use Tulsa template  
   - Large city (500k+): Adapt the templates

2. **Copy an existing notebook:**
   ```bash
   # In Jupyter Lab, duplicate an existing notebook
   # Right-click on modesto_spatial_dbscan.ipynb → Duplicate
   ```

3. **Update the coordinates:**
   ```python
   # Replace these with your city's coordinates
   CITY_NAME = "Your City, State"
   DOWNTOWN_LAT = 40.7128  # Your city's latitude
   DOWNTOWN_LON = -74.0060  # Your city's longitude
   UTM_EPSG = 32618  # Your UTM zone (use UTM zone calculator)
   ```

4. **Run the analysis:**
   - Execute all cells
   - View your interactive map
   - Analyze the clustering results

### Option B: Start from Scratch
1. **Create a new notebook:**
   - File → New → Notebook
   - Choose Python 3 kernel

2. **Follow the template structure:**
   ```python
   # Cell 1: Imports and setup
   import numpy as np
   import geopandas as gpd
   import folium
   from sklearn.cluster import DBSCAN
   
   # Cell 2: Define your city parameters
   CITY_NAME = "Your City"
   CENTER_LAT = 40.7128
   CENTER_LON = -74.0060
   
   # Cell 3: Generate or import data
   # (See creating-notebooks.md for detailed examples)
   
   # Cell 4: Apply DBSCAN clustering
   # Cell 5: Create visualizations
   # Cell 6: Export results
   ```

## 🎯 Common Use Cases

### Crime Hotspot Analysis
```python
# Perfect for public safety applications
DBSCAN_EPS = 400  # 400m radius for crime clusters
MIN_SAMPLES = 6   # Minimum incidents to form hotspot

# Focus on high-activity areas
locations = {
    'entertainment_district': (lat, lon),
    'transit_stations': (lat, lon),
    'shopping_areas': (lat, lon)
}
```

### Business Location Analysis
```python
# Ideal for commercial planning
DBSCAN_EPS = 250  # 250m radius for business districts
MIN_SAMPLES = 8   # Minimum businesses for commercial cluster

# Target commercial zones
locations = {
    'main_street': (lat, lon),
    'shopping_centers': (lat, lon),
    'business_parks': (lat, lon)
}
```

### Emergency Services Planning
```python
# Great for response optimization
DBSCAN_EPS = 800  # 800m radius for emergency clusters
MIN_SAMPLES = 4   # Minimum incidents for planning

# Focus on high-risk areas
locations = {
    'hospital_district': (lat, lon),
    'industrial_zones': (lat, lon),
    'highway_corridors': (lat, lon)
}
```

## 🗺️ Finding Your City's Coordinates

### Method 1: Google Maps
1. Go to [Google Maps](https://maps.google.com)
2. Search for your city
3. Right-click on the city center
4. Select "What's here?"
5. Copy the coordinates (latitude, longitude)

### Method 2: LatLong.net
1. Visit [LatLong.net](https://www.latlong.net/)
2. Enter your city name
3. Copy the decimal coordinates

### Method 3: OpenStreetMap
1. Go to [OpenStreetMap](https://www.openstreetmap.org)
2. Search for your city
3. The URL will show coordinates: `#map=zoom/lat/lon`

## 🌐 Determining Your UTM Zone

### Quick Calculator
Use this formula for a rough estimate:
```python
utm_zone = int((longitude + 180) / 6) + 1
```

### Online Tools
- [UTM Zone Map](https://www.dmap.co.uk/utmworld.htm)
- [UTM Coordinate Converter](https://www.latlong.net/lat-long-utm.html)

### Common UTM Zones (North America)
| Region | Longitude Range | UTM Zone | EPSG Code |
|--------|----------------|----------|-----------|
| West Coast | -126° to -120° | 10 | 32610 |
| California | -120° to -114° | 11 | 32611 |
| Mountain West | -114° to -108° | 12 | 32612 |
| Central Plains | -102° to -96° | 14 | 32614 |
| Great Lakes | -90° to -84° | 16 | 32616 |
| East Coast | -78° to -72° | 18 | 32618 |

## ⚙️ Parameter Tuning Guide

### DBSCAN Parameters

**eps (distance threshold):**
- Small towns: 200-400 meters
- Cities: 500-800 meters  
- Metro areas: 1000-2000 meters

**min_samples (minimum cluster size):**
- Sparse data: 3-5 points
- Medium density: 5-8 points
- Dense data: 8-15 points

### Quick Parameter Test
```python
# Test different parameters quickly
eps_values = [300, 500, 800]
min_samples_values = [4, 6, 8]

for eps in eps_values:
    for min_samples in min_samples_values:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(coords)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        print(f"eps={eps}, min_samples={min_samples}: {n_clusters} clusters")
```

## 🎨 Quick Visualization Tips

### Instant Interactive Map
```python
# One-line interactive map
gdf.explore(column='cluster_id', cmap='viridis', tiles='CartoDB positron')
```

### Quick Static Plot
```python
# Simple static visualization
gdf.plot(column='cluster_id', cmap='tab10', figsize=(10, 8), legend=True)
plt.title(f'Clusters in {CITY_NAME}')
plt.show()
```

### Export Your Map
```python
# Save interactive map
m = gdf.explore(column='cluster_id', cmap='viridis')
m.save(f'{CITY_NAME.lower().replace(" ", "_")}_map.html')

# Save static image
fig, ax = plt.subplots(figsize=(12, 8))
gdf.plot(column='cluster_id', ax=ax, legend=True)
plt.savefig(f'{CITY_NAME.lower().replace(" ", "_")}_clusters.png', dpi=300)
```

## 🆘 Troubleshooting

### Common Issues

**"No clusters found"**
- Reduce `eps` parameter
- Reduce `min_samples` parameter
- Check if coordinates are correct

**"Points in wrong location"**
- Verify coordinate order (latitude, longitude)
- Check UTM zone is correct for your region
- Ensure CRS is properly set

**"Map doesn't display"**
- Refresh the browser
- Check JavaScript console for errors
- Try a different tile provider

**"Container won't start"**
- Check if port 8888 is already in use
- Try a different port: `-p 8889:8888`
- Restart Docker service

### Getting Help

1. **Check the documentation:**
   - [Creating Custom Notebooks](user-guides/creating-notebooks.md)
   - [City Analysis Templates](user-guides/city-analysis-templates.md)

2. **Review examples:**
   - Look at existing notebooks in the `notebooks/` folder
   - Compare with similar-sized cities

3. **Ask for help:**
   - Open an issue on GitHub
   - Include your city name and coordinates
   - Share any error messages

## 🚀 Next Steps

Once you have a basic analysis working:

1. **Enhance your analysis:**
   - Add real data (see [Data Import Guide](user-guides/data-import.md))
   - Try different clustering algorithms
   - Create custom visualizations

2. **Share your work:**
   - Export your results
   - Create a presentation
   - Contribute back to the community

3. **Explore advanced features:**
   - Multi-city comparisons
   - Temporal analysis
   - 3D visualizations

## 📚 Learn More

- **[Complete Documentation](README.md)** - Full documentation index
- **[Creating Custom Notebooks](user-guides/creating-notebooks.md)** - Detailed step-by-step guide
- **[Visualization Guide](user-guides/visualization-guide.md)** - Advanced mapping techniques
- **[Basic Spatial Analysis](examples/basic-spatial-analysis.md)** - Fundamental concepts

---

**Ready to analyze your city? Start with the 5-minute setup above and you'll be creating spatial insights in no time!** 🗺️✨
