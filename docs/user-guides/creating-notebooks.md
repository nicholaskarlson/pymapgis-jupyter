# 📓 Creating Custom Notebooks: Complete Guide

This comprehensive guide will walk you through creating your own spatial analysis notebooks for any city or region using the PyMapGIS Jupyter environment.

## 🎯 Overview

Creating a custom notebook involves:
1. **Planning your analysis** - Define objectives and data requirements
2. **Setting up the notebook structure** - Organize cells and sections
3. **Configuring geographic parameters** - Coordinates, projections, and boundaries
4. **Implementing spatial analysis** - Clustering, visualization, and statistics
5. **Testing and validation** - Ensure reproducible results

## 📋 Prerequisites

- Access to PyMapGIS Jupyter environment (Docker container running)
- Basic understanding of Python and Jupyter notebooks
- Geographic coordinates for your target area
- Understanding of your analysis objectives

## 🗺️ Step 1: Planning Your Analysis

### Define Your Objectives
Before creating a notebook, clearly define:
- **What spatial patterns are you looking for?**
- **What type of data will you analyze?** (points, polygons, raster)
- **What clustering parameters make sense for your area?**
- **What visualizations will be most effective?**

### Choose Your Geographic Area
Identify:
- **City/region name** and key landmarks
- **Central coordinates** (latitude, longitude)
- **Appropriate UTM zone** for accurate distance calculations
- **Boundary extent** for noise generation

### Example Planning Template
```markdown
## Analysis Plan: [Your City Name]

**Objective**: Identify spatial clusters of [incident type] in [city name]

**Key Locations**:
- Downtown: [lat, lon]
- Airport: [lat, lon] 
- University: [lat, lon]

**Parameters**:
- UTM Zone: [zone number]
- DBSCAN eps: [distance in meters]
- DBSCAN min_samples: [minimum points]
```

## 📝 Step 2: Notebook Structure Template

### Standard Notebook Sections

1. **Title and Introduction**
2. **Library Imports**
3. **Data Generation/Import**
4. **Spatial Projection**
5. **Clustering Analysis**
6. **Visualization**
7. **Results Export**
8. **Summary and Next Steps**

### Recommended Cell Structure
```python
# Cell 1: Title and Markdown Introduction
# Cell 2: Library imports and setup
# Cell 3: Geographic parameters and coordinates
# Cell 4: Data generation or import
# Cell 5: Coordinate system projection
# Cell 6: DBSCAN clustering
# Cell 7: Results analysis
# Cell 8: Interactive map creation
# Cell 9: Static visualizations
# Cell 10: Data export
# Cell 11: Summary and conclusions
```

## 🌍 Step 3: Geographic Configuration

### Finding Coordinates
Use these resources to find accurate coordinates:
- **Google Maps**: Right-click → "What's here?"
- **LatLong.net**: Search by address or landmark
- **OpenStreetMap**: Search and inspect coordinates

### UTM Zone Selection
Determine the correct UTM zone for your area:
- **North America**: Use [UTM Zone Map](https://www.dmap.co.uk/utmworld.htm)
- **Formula**: Zone = floor((longitude + 180) / 6) + 1
- **EPSG Codes**: UTM zones use EPSG:326XX (north) or EPSG:327XX (south)

### Example Geographic Setup
```python
# Geographic parameters for [Your City]
CITY_NAME = "Your City, State/Country"
DOWNTOWN_LAT = 40.7128  # Replace with actual coordinates
DOWNTOWN_LON = -74.0060
UTM_EPSG = 32618  # Replace with correct UTM zone

# Key locations for hotspot generation
locations = {
    'downtown': (DOWNTOWN_LAT, DOWNTOWN_LON),
    'airport': (40.6892, -74.1745),  # Example coordinates
    'university': (40.7282, -73.9942)  # Example coordinates
}
```

## 🔬 Step 4: Data Generation Patterns

### Hotspot Generation Template
```python
import numpy as np
from shapely.geometry import Point

# Set random seed for reproducibility
np.random.seed(42)

# Generate hotspot data
def create_hotspot(center_lat, center_lon, num_points, spread=0.002):
    """Create a cluster of points around a center location."""
    points = []
    for _ in range(num_points):
        lat = np.random.normal(center_lat, spread)
        lon = np.random.normal(center_lon, spread)
        points.append(Point(lon, lat))
    return points

# Create hotspots for each location
downtown_points = create_hotspot(
    locations['downtown'][0], 
    locations['downtown'][1], 
    50,  # Number of points
    0.002  # Spread (approximately 200m)
)

airport_points = create_hotspot(
    locations['airport'][0],
    locations['airport'][1],
    40,
    0.002
)

# Combine all hotspots
all_hotspots = downtown_points + airport_points

# Generate regional noise
noise_points = []
for _ in range(30):
    # Adjust bounds for your region
    lat = np.random.uniform(DOWNTOWN_LAT - 0.1, DOWNTOWN_LAT + 0.1)
    lon = np.random.uniform(DOWNTOWN_LON - 0.1, DOWNTOWN_LON + 0.1)
    noise_points.append(Point(lon, lat))

# Combine all points
all_points = all_hotspots + noise_points
```

### Creating GeoDataFrame
```python
import geopandas as gpd
import pandas as pd

# Create GeoDataFrame
gdf = gpd.GeoDataFrame({
    'id': range(len(all_points)),
    'geometry': all_points
}, crs='EPSG:4326')

# Add metadata
gdf['point_type'] = (['hotspot'] * len(all_hotspots) + 
                     ['noise'] * len(noise_points))

print(f"✅ Generated {len(gdf)} points for {CITY_NAME}")
```

## 🎯 Step 5: Clustering Implementation

### DBSCAN Configuration
```python
from sklearn.cluster import DBSCAN

# Project to UTM for accurate distance calculations
gdf_utm = gdf.to_crs(f'EPSG:{UTM_EPSG}')

# Extract coordinates for clustering
coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])

# Configure DBSCAN parameters
# eps: maximum distance between points in a cluster (meters)
# min_samples: minimum points required to form a cluster
eps_meters = 500  # Adjust based on your city size
min_samples = 5   # Adjust based on expected cluster density

# Apply DBSCAN
dbscan = DBSCAN(eps=eps_meters, min_samples=min_samples)
cluster_labels = dbscan.fit_predict(coords)

# Add cluster labels to GeoDataFrame
gdf_utm['cluster_id'] = cluster_labels
gdf['cluster_id'] = cluster_labels

print(f"✅ DBSCAN clustering complete")
print(f"Found {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)} clusters")
print(f"Noise points: {sum(cluster_labels == -1)}")
```

## 📊 Step 6: Visualization

### Interactive Map Creation
```python
import folium
from folium import plugins

# Create base map centered on your city
center_lat, center_lon = locations['downtown']
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles='CartoDB positron'
)

# Color mapping for clusters
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
          'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']

# Add points to map
for idx, row in gdf.iterrows():
    cluster_id = row['cluster_id']
    
    if cluster_id == -1:
        # Noise points
        color = 'gray'
        popup_text = f"Noise Point {row['id']}"
    else:
        # Cluster points
        color = colors[cluster_id % len(colors)]
        popup_text = f"Cluster {cluster_id}, Point {row['id']}"
    
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=6,
        popup=popup_text,
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.7
    ).add_to(m)

# Add title
title_html = f'''
<h3 align="center" style="font-size:20px"><b>Spatial Clusters in {CITY_NAME}</b></h3>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Display map
m
```

### Static Visualizations
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Cluster statistics
cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()

# Create subplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Bar plot of cluster sizes
cluster_counts.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title(f'Cluster Sizes in {CITY_NAME}')
ax1.set_xlabel('Cluster ID (-1 = Noise)')
ax1.set_ylabel('Number of Points')

# Scatter plot of clusters
gdf_utm.plot(column='cluster_id', cmap='viridis', ax=ax2, 
             legend=True, markersize=50, alpha=0.7)
ax2.set_title(f'Spatial Distribution of Clusters')
ax2.set_xlabel('UTM Easting (m)')
ax2.set_ylabel('UTM Northing (m)')

plt.tight_layout()
plt.show()
```

## 💾 Step 7: Data Export

### Export Results
```python
# Export to various formats
output_prefix = CITY_NAME.lower().replace(' ', '_').replace(',', '')

# CSV export
gdf.to_csv(f'notebooks/{output_prefix}_dbscan_results.csv', index=False)

# GeoJSON export  
gdf.to_file(f'notebooks/{output_prefix}_dbscan_results.geojson', driver='GeoJSON')

# Summary statistics
summary = {
    'city': CITY_NAME,
    'total_points': len(gdf),
    'num_clusters': len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
    'noise_points': sum(cluster_labels == -1),
    'eps_meters': eps_meters,
    'min_samples': min_samples,
    'utm_epsg': UTM_EPSG
}

# Save summary
import json
with open(f'notebooks/{output_prefix}_analysis_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"✅ Results exported:")
print(f"   - CSV: {output_prefix}_dbscan_results.csv")
print(f"   - GeoJSON: {output_prefix}_dbscan_results.geojson") 
print(f"   - Summary: {output_prefix}_analysis_summary.json")
```

## ✅ Step 8: Testing and Validation

### Validation Checklist
- [ ] **Coordinates are correct** - Points appear in expected locations
- [ ] **Clustering makes sense** - Clusters align with generated hotspots
- [ ] **Map displays properly** - Interactive map loads and shows data
- [ ] **Exports work** - Files are created and contain expected data
- [ ] **Documentation is clear** - Markdown cells explain each step

### Common Issues and Solutions

**Issue**: Points appear in wrong location
- **Solution**: Check coordinate order (lat, lon vs lon, lat)
- **Solution**: Verify UTM zone is correct for your region

**Issue**: No clusters found
- **Solution**: Reduce `eps` parameter or `min_samples`
- **Solution**: Check if points are too spread out

**Issue**: Map doesn't display
- **Solution**: Ensure folium is installed and updated
- **Solution**: Check for JavaScript errors in browser console

## 🚀 Next Steps

After creating your notebook:

1. **Test with different parameters** - Try various eps and min_samples values
2. **Add real data** - Replace simulated data with actual datasets
3. **Enhance visualizations** - Add legends, better styling, multiple views
4. **Share your work** - Contribute back to the community

## 📚 Additional Resources

- **[City Analysis Templates](city-analysis-templates.md)** - Pre-built templates for common scenarios
- **[Data Import Guide](data-import.md)** - Working with real spatial datasets
- **[Visualization Guide](visualization-guide.md)** - Advanced mapping techniques
- **[PyMapGIS Documentation](../api-reference/pymapgis-functions.md)** - Complete function reference

---

*Ready to create your first custom notebook? Start with the template above and adapt it to your specific city and analysis needs!*
