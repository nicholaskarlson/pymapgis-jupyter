# 📥 Data Import Guide

This guide covers importing your own spatial datasets into the PyMapGIS Jupyter environment, replacing simulated data with real-world information.

## 🎯 Overview

The PyMapGIS environment supports various spatial data formats and provides tools for:
- **Loading spatial files** (Shapefile, GeoJSON, CSV with coordinates)
- **Connecting to spatial databases** (PostGIS, SpatiaLite)
- **Accessing web services** (WFS, REST APIs)
- **Processing raster data** (GeoTIFF, NetCDF)

## 📁 Supported Data Formats

### Vector Data Formats
- **Shapefile** (.shp, .shx, .dbf, .prj)
- **GeoJSON** (.geojson, .json)
- **CSV with coordinates** (.csv)
- **KML/KMZ** (.kml, .kmz)
- **GeoPackage** (.gpkg)
- **File Geodatabase** (.gdb)

### Raster Data Formats
- **GeoTIFF** (.tif, .tiff)
- **NetCDF** (.nc)
- **HDF5** (.h5, .hdf5)
- **JPEG2000** (.jp2)

### Database Connections
- **PostGIS** (PostgreSQL with spatial extension)
- **SpatiaLite** (SQLite with spatial extension)
- **MongoDB** (with geospatial features)

## 🔄 Data Import Methods

### Method 1: File Upload to Container

#### Upload Files via Jupyter Interface
1. **Access Jupyter Lab** at `http://localhost:8888`
2. **Navigate to the file browser** (left sidebar)
3. **Click the upload button** (up arrow icon)
4. **Select your spatial data files**
5. **Upload to the `notebooks/` directory**

#### Upload via Docker Volume Mount
```bash
# Mount local data directory to container
docker run -p 8888:8888 \
  -v /path/to/your/data:/home/jovyan/data \
  -v /path/to/notebooks:/home/jovyan/notebooks \
  nicholaskarlson/pymapgis-jupyter:secure
```

### Method 2: Direct File Loading

#### Loading Shapefiles
```python
import geopandas as gpd

# Load shapefile
gdf = gpd.read_file('data/your_shapefile.shp')

# Check the data
print(f"Loaded {len(gdf)} features")
print(f"CRS: {gdf.crs}")
print(f"Columns: {list(gdf.columns)}")
print(f"Geometry types: {gdf.geometry.type.unique()}")

# Display first few rows
gdf.head()
```

#### Loading GeoJSON
```python
# Load GeoJSON file
gdf = gpd.read_file('data/your_data.geojson')

# Or load from URL
url = 'https://example.com/data.geojson'
gdf = gpd.read_file(url)
```

#### Loading CSV with Coordinates
```python
import pandas as pd
from shapely.geometry import Point

# Load CSV file
df = pd.read_csv('data/your_data.csv')

# Create geometry from lat/lon columns
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

# Alternative: specify coordinate columns
gdf = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df.longitude, df.latitude),
    crs='EPSG:4326'
)
```

### Method 3: Database Connections

#### PostGIS Connection
```python
import psycopg2
from sqlalchemy import create_engine

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'port': '5432'
}

# Create connection string
conn_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"

# Load spatial data from PostGIS
sql_query = """
SELECT * FROM your_spatial_table 
WHERE ST_Intersects(geom, ST_MakeEnvelope(-180, -90, 180, 90, 4326))
"""

gdf = gpd.read_postgis(sql_query, conn_string, geom_col='geom')
```

#### SpatiaLite Connection
```python
import sqlite3

# Connect to SpatiaLite database
conn = sqlite3.connect('data/your_database.sqlite')

# Load spatial data
gdf = gpd.read_file('data/your_database.sqlite', layer='your_layer')
```

### Method 4: Web Services

#### Web Feature Service (WFS)
```python
# Load data from WFS endpoint
wfs_url = 'https://example.com/geoserver/wfs'
params = {
    'service': 'WFS',
    'version': '2.0.0',
    'request': 'GetFeature',
    'typeName': 'your_layer',
    'outputFormat': 'application/json'
}

gdf = gpd.read_file(wfs_url, **params)
```

#### REST API with Coordinates
```python
import requests
import json

# Fetch data from REST API
api_url = 'https://api.example.com/spatial-data'
response = requests.get(api_url)
data = response.json()

# Convert to GeoDataFrame
features = []
for item in data['features']:
    features.append({
        'id': item['id'],
        'name': item['properties']['name'],
        'geometry': Point(item['geometry']['coordinates'])
    })

gdf = gpd.GeoDataFrame(features, crs='EPSG:4326')
```

## 🔧 Data Preprocessing

### Coordinate Reference Systems (CRS)

#### Check and Transform CRS
```python
# Check current CRS
print(f"Current CRS: {gdf.crs}")

# Transform to WGS84 (EPSG:4326) for mapping
if gdf.crs != 'EPSG:4326':
    gdf_wgs84 = gdf.to_crs('EPSG:4326')
else:
    gdf_wgs84 = gdf.copy()

# Transform to UTM for distance calculations
# Determine appropriate UTM zone for your area
utm_epsg = 32618  # Example: UTM Zone 18N
gdf_utm = gdf.to_crs(f'EPSG:{utm_epsg}')
```

#### Auto-detect UTM Zone
```python
def get_utm_epsg(longitude):
    """Get UTM EPSG code from longitude."""
    utm_zone = int((longitude + 180) / 6) + 1
    # Assuming Northern Hemisphere
    epsg_code = 32600 + utm_zone
    return epsg_code

# Get center longitude of your data
center_lon = gdf_wgs84.geometry.centroid.x.mean()
utm_epsg = get_utm_epsg(center_lon)
gdf_utm = gdf_wgs84.to_crs(f'EPSG:{utm_epsg}')
```

### Data Cleaning and Validation

#### Remove Invalid Geometries
```python
# Check for invalid geometries
invalid_geoms = ~gdf.geometry.is_valid
print(f"Invalid geometries: {invalid_geoms.sum()}")

# Remove or fix invalid geometries
gdf_clean = gdf[gdf.geometry.is_valid].copy()

# Or attempt to fix invalid geometries
gdf['geometry'] = gdf.geometry.buffer(0)  # Often fixes topology issues
```

#### Handle Missing Values
```python
# Check for missing values
print("Missing values per column:")
print(gdf.isnull().sum())

# Remove rows with missing geometries
gdf_clean = gdf.dropna(subset=['geometry'])

# Fill missing attribute values
gdf['category'] = gdf['category'].fillna('unknown')
```

#### Filter by Spatial Extent
```python
# Define bounding box for your area of interest
min_lon, min_lat = -122.5, 37.7  # Example: San Francisco area
max_lon, max_lat = -122.3, 37.8

# Filter data to bounding box
mask = (
    (gdf_wgs84.geometry.x >= min_lon) & 
    (gdf_wgs84.geometry.x <= max_lon) &
    (gdf_wgs84.geometry.y >= min_lat) & 
    (gdf_wgs84.geometry.y <= max_lat)
)

gdf_filtered = gdf_wgs84[mask].copy()
print(f"Filtered to {len(gdf_filtered)} features in bounding box")
```

### Data Type Conversions

#### Convert Polygon/Line Data to Points
```python
# Convert polygons to centroids
if gdf.geometry.type.iloc[0] in ['Polygon', 'MultiPolygon']:
    gdf['geometry'] = gdf.geometry.centroid

# Convert lines to points (start points)
elif gdf.geometry.type.iloc[0] in ['LineString', 'MultiLineString']:
    gdf['geometry'] = gdf.geometry.apply(lambda x: Point(x.coords[0]))
```

#### Aggregate Point Data
```python
# Group nearby points (useful for dense datasets)
from sklearn.cluster import DBSCAN

# Get coordinates
coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])

# Cluster nearby points
clustering = DBSCAN(eps=100, min_samples=1)  # 100m radius
cluster_labels = clustering.fit_predict(coords)

# Aggregate by cluster
gdf['cluster'] = cluster_labels
aggregated = gdf.groupby('cluster').agg({
    'geometry': lambda x: x.iloc[0],  # Take first geometry
    'value': 'sum',  # Sum numeric values
    'category': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else x.iloc[0]  # Most common category
}).reset_index()

aggregated_gdf = gpd.GeoDataFrame(aggregated, crs=gdf.crs)
```

## 📊 Data Integration with Analysis

### Adapting Existing Notebooks

#### Replace Simulated Data
```python
# Instead of generating simulated data:
# downtown_points = create_hotspot(...)

# Load your real data:
gdf = gpd.read_file('data/your_real_data.shp')

# Ensure proper CRS
gdf_wgs84 = gdf.to_crs('EPSG:4326')
gdf_utm = gdf.to_crs('EPSG:32618')  # Use appropriate UTM zone

# Extract coordinates for clustering
coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])

# Continue with existing DBSCAN analysis...
```

#### Customize Analysis Parameters
```python
# Adjust DBSCAN parameters based on your data characteristics
data_extent = gdf_utm.total_bounds
width = data_extent[2] - data_extent[0]  # Width in meters
height = data_extent[3] - data_extent[1]  # Height in meters

# Suggest eps based on data extent
suggested_eps = min(width, height) / 20  # 5% of smaller dimension
print(f"Suggested eps: {suggested_eps:.0f} meters")

# Adjust min_samples based on data density
points_per_km2 = len(gdf) / ((width * height) / 1000000)
suggested_min_samples = max(3, int(points_per_km2 / 10))
print(f"Suggested min_samples: {suggested_min_samples}")
```

### Working with Attributes

#### Use Attribute-Based Filtering
```python
# Filter by attribute values
if 'category' in gdf.columns:
    # Analyze specific categories
    crime_data = gdf[gdf['category'].isin(['theft', 'burglary', 'assault'])]
    
    # Separate analysis by category
    for category in gdf['category'].unique():
        category_data = gdf[gdf['category'] == category]
        print(f"{category}: {len(category_data)} points")
```

#### Temporal Analysis
```python
# If your data has timestamps
if 'timestamp' in gdf.columns:
    # Convert to datetime
    gdf['datetime'] = pd.to_datetime(gdf['timestamp'])
    
    # Filter by time period
    start_date = '2024-01-01'
    end_date = '2024-12-31'
    
    mask = (gdf['datetime'] >= start_date) & (gdf['datetime'] <= end_date)
    gdf_filtered = gdf[mask]
    
    # Analyze by time periods
    gdf['month'] = gdf['datetime'].dt.month
    monthly_counts = gdf.groupby('month').size()
```

## 🔍 Data Quality Assessment

### Validation Checklist
```python
def assess_data_quality(gdf):
    """Comprehensive data quality assessment."""
    print("=== DATA QUALITY ASSESSMENT ===")
    
    # Basic statistics
    print(f"Total features: {len(gdf)}")
    print(f"CRS: {gdf.crs}")
    print(f"Geometry types: {gdf.geometry.type.value_counts().to_dict()}")
    
    # Spatial extent
    bounds = gdf.total_bounds
    print(f"Spatial extent: {bounds}")
    
    # Missing values
    missing = gdf.isnull().sum()
    if missing.sum() > 0:
        print(f"Missing values:\n{missing[missing > 0]}")
    
    # Invalid geometries
    invalid = ~gdf.geometry.is_valid
    if invalid.sum() > 0:
        print(f"Invalid geometries: {invalid.sum()}")
    
    # Duplicate geometries
    duplicates = gdf.geometry.duplicated().sum()
    if duplicates > 0:
        print(f"Duplicate geometries: {duplicates}")
    
    # Attribute summary
    print("\n=== ATTRIBUTE SUMMARY ===")
    for col in gdf.columns:
        if col != 'geometry':
            if gdf[col].dtype in ['object']:
                unique_vals = gdf[col].nunique()
                print(f"{col}: {unique_vals} unique values")
            else:
                print(f"{col}: {gdf[col].describe()}")

# Run assessment
assess_data_quality(gdf)
```

## 🚀 Performance Optimization

### Large Dataset Handling
```python
# For very large datasets (>100k points)

# 1. Spatial indexing
gdf_indexed = gdf.sindex

# 2. Chunked processing
chunk_size = 10000
for i in range(0, len(gdf), chunk_size):
    chunk = gdf.iloc[i:i+chunk_size]
    # Process chunk...

# 3. Simplified geometries
gdf['geometry'] = gdf.geometry.simplify(tolerance=10)  # 10m tolerance

# 4. Spatial sampling
sample_fraction = 0.1  # Use 10% of data
gdf_sample = gdf.sample(frac=sample_fraction, random_state=42)
```

## 📚 Example Workflows

### Complete Import Workflow
```python
# Complete workflow example
def import_and_prepare_data(file_path, target_utm_epsg):
    """Complete data import and preparation workflow."""
    
    # 1. Load data
    print("Loading data...")
    gdf = gpd.read_file(file_path)
    
    # 2. Quality assessment
    assess_data_quality(gdf)
    
    # 3. Clean data
    print("Cleaning data...")
    gdf = gdf[gdf.geometry.is_valid]
    gdf = gdf.dropna(subset=['geometry'])
    
    # 4. Transform CRS
    print("Transforming coordinates...")
    gdf_wgs84 = gdf.to_crs('EPSG:4326')
    gdf_utm = gdf.to_crs(f'EPSG:{target_utm_epsg}')
    
    # 5. Prepare for analysis
    coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])
    
    print(f"✅ Data prepared: {len(gdf)} features ready for analysis")
    
    return gdf_wgs84, gdf_utm, coords

# Use the workflow
gdf_wgs84, gdf_utm, coords = import_and_prepare_data(
    'data/your_data.shp', 
    32618  # UTM Zone 18N
)
```

## 🆘 Troubleshooting

### Common Issues and Solutions

**Issue**: "CRS not found" error
```python
# Solution: Manually set CRS
gdf.crs = 'EPSG:4326'  # or appropriate EPSG code
```

**Issue**: "Invalid geometry" errors
```python
# Solution: Fix geometries
gdf['geometry'] = gdf.geometry.buffer(0)
gdf = gdf[gdf.geometry.is_valid]
```

**Issue**: Memory errors with large files
```python
# Solution: Process in chunks or sample data
gdf_sample = gdf.sample(n=10000, random_state=42)
```

**Issue**: Coordinate order confusion
```python
# Solution: Check coordinate order
print(f"First point: {gdf.geometry.iloc[0]}")
# Ensure longitude (x) comes before latitude (y)
```

## 📚 Additional Resources

- **[Creating Custom Notebooks](creating-notebooks.md)** - Using imported data in analysis
- **[City Analysis Templates](city-analysis-templates.md)** - Adapting templates for real data
- **[Visualization Guide](visualization-guide.md)** - Mapping imported datasets

---

*Ready to import your own data? Start with the format that matches your dataset and follow the appropriate workflow above.*
