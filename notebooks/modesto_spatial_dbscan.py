#!/usr/bin/env python3
"""
Spatial DBSCAN Analysis - Modesto, California

This script demonstrates spatial clustering using DBSCAN on simulated incident 
data in Modesto, California. Designed to run in the secure Docker environment:
nicholaskarlson/pymapgis-jupyter:secure

Author: Nicholas Karlson
Date: 2025-01-04
"""

# ==============================================================================
# Import required libraries (pre-installed in Docker environment)
# ==============================================================================
import pymapgis as pmg
from pymapgis.ml import SpatialDBSCAN
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import numpy as np

print("✅ Using pre-installed libraries from secure Docker environment.")
print("🐳 Running in nicholaskarlson/pymapgis-jupyter:secure")
print("🔒 Security-hardened container with non-root user")
print("=" * 60)

# ==============================================================================
# 1. Simulate incidents: two Modesto hotspots + regional noise
# ==============================================================================
print("\n📍 Generating simulated incident data for Modesto, California...")
np.random.seed(42)

# Hotspot 1 – Downtown Modesto (around 10th & I Street)
print("   Creating Downtown Modesto hotspot...")
downtown_modesto = [
    Point(np.random.normal(-121.0018, 0.002),   # lon  (≈200 m spread)
          np.random.normal(37.6391, 0.002))     # lat
    for _ in range(50)
]

# Hotspot 2 – Vintage Faire Mall area (North Modesto)
print("   Creating Vintage Faire Mall hotspot...")
vintage_faire = [
    Point(np.random.normal(-121.0244, 0.002),   # lon
          np.random.normal(37.6764, 0.002))     # lat
    for _ in range(40)
]

# Background noise across Stanislaus County
print("   Adding regional noise across Stanislaus County...")
noise = [
    Point(np.random.uniform(-121.3, -120.7),   # Stanislaus County longitudes
          np.random.uniform(37.4, 37.8))       # Stanislaus County latitudes
    for _ in range(40)
]

# Create GeoDataFrame
incidents_gdf = gpd.GeoDataFrame(
    geometry=downtown_modesto + vintage_faire + noise,
    crs="EPSG:4326"
)
incidents_gdf["report_id"] = range(len(incidents_gdf))

print(f"✅ Generated {len(incidents_gdf)} simulated incidents in Modesto area.")

# ==============================================================================
# 2. Re-project to metres for accurate distance calculations
# ==============================================================================
print("\n🗺️  Reprojecting coordinates...")
# California Zone 3 NAD83 / UTM 10N (appropriate for Central Valley)
incidents_m = incidents_gdf.to_crs(epsg=26910)
print("✅ Reprojected to UTM Zone 10N for accurate distance calculations.")

# ==============================================================================
# 3. Spatial DBSCAN clustering
# ==============================================================================
print("\n🚀 Running Spatial DBSCAN clustering...")
X_dummy = pd.DataFrame(index=incidents_m.index)  # geometry-only model

db = SpatialDBSCAN(eps=250,  # 250 m neighbourhood radius
                   min_samples=5,
                   spatial_weight=1.0)
db.fit(X_dummy, geometry=incidents_m.geometry)

incidents_gdf["cluster_id"] = db.labels_  # copy labels back to WGS-84

print("✅ DBSCAN clustering complete.")

# ==============================================================================
# 4. Analysis Results
# ==============================================================================
print("\n📊 SPATIAL DBSCAN ANALYSIS RESULTS")
print("=" * 50)
print(f"Location: Modesto, California")
print(f"Total incidents: {len(incidents_gdf)}")
print(f"Clusters found: {len(incidents_gdf[incidents_gdf['cluster_id'] >= 0]['cluster_id'].unique())}")
print(f"Noise points: {len(incidents_gdf[incidents_gdf['cluster_id'] == -1])}")
print(f"DBSCAN parameters: eps=250m, min_samples=5")
print(f"Coordinate system: WGS84 (EPSG:4326)")
print(f"Analysis projection: UTM Zone 10N (EPSG:26910)")

print("\n--- Cluster Distribution ---")
cluster_counts = incidents_gdf["cluster_id"].value_counts().sort_index()
for cluster_id, count in cluster_counts.items():
    if cluster_id == -1:
        print(f"Noise points: {count}")
    else:
        print(f"Cluster {cluster_id}: {count} incidents")
print("---------------------------")

# Show cluster statistics
cluster_stats = incidents_gdf[incidents_gdf['cluster_id'] >= 0].groupby('cluster_id').size()
if len(cluster_stats) > 0:
    print("\n🎯 Identified Hotspots:")
    for cluster_id, size in cluster_stats.items():
        # Get cluster centroid for location description
        cluster_points = incidents_gdf[incidents_gdf['cluster_id'] == cluster_id]
        centroid_lon = cluster_points.geometry.x.mean()
        centroid_lat = cluster_points.geometry.y.mean()
        
        # Determine location based on coordinates
        if abs(centroid_lon - (-121.0018)) < 0.01 and abs(centroid_lat - 37.6391) < 0.01:
            location = "Downtown Modesto area"
        elif abs(centroid_lon - (-121.0244)) < 0.01 and abs(centroid_lat - 37.6764) < 0.01:
            location = "Vintage Faire Mall area"
        else:
            location = f"({centroid_lat:.4f}, {centroid_lon:.4f})"
            
        print(f"   Cluster {cluster_id}: {size} incidents near {location}")

# ==============================================================================
# 5. Save results (optional)
# ==============================================================================
print("\n💾 Saving results...")
try:
    # Save to CSV
    output_file = "/home/jupyter/notebooks/modesto_dbscan_results.csv"
    incidents_gdf.to_csv(output_file, index=False)
    print(f"✅ Results saved to: {output_file}")
    
    # Save to GeoJSON for mapping
    geojson_file = "/home/jupyter/notebooks/modesto_dbscan_results.geojson"
    incidents_gdf.to_file(geojson_file, driver='GeoJSON')
    print(f"✅ GeoJSON saved to: {geojson_file}")
    
except Exception as e:
    print(f"⚠️  Could not save files: {e}")
    print("   (This is normal if running outside the Docker container)")

# ==============================================================================
# 6. Interactive Map Generation (if in Jupyter environment)
# ==============================================================================
print("\n🎨 Generating interactive map...")
try:
    # Check if we're in a Jupyter environment
    from IPython.display import display
    
    # Create interactive map
    m = incidents_gdf.explore(
        column="cluster_id",
        cmap="viridis",
        categorical=True,
        tooltip=["report_id", "cluster_id"],
        style_kwds={"radius": 6},
        tiles="CartoDB positron"
    )
    
    # Center the map on Modesto
    m.location = [37.6391, -121.0018]  # Downtown Modesto coordinates
    m.zoom_start = 12
    
    display(m)
    print("🎉 Interactive map displayed above!")
    print("📍 Map centered on Downtown Modesto, California")
    print("   • Green/Blue points: Clustered incidents")
    print("   • Purple points: Noise (isolated incidents)")
    
except ImportError:
    print("📋 Running in non-Jupyter environment - map display skipped")
    print("   To view the interactive map, run this in Jupyter Lab:")
    print("   1. Start container: docker run -p 8888:8888 nicholaskarlson/pymapgis-jupyter:secure")
    print("   2. Open browser: http://localhost:8888")
    print("   3. Run the notebook version: modesto_spatial_dbscan.ipynb")

print("\n" + "=" * 60)
print("✅ Spatial DBSCAN analysis complete!")
print("🔍 Check the results above for identified crime hotspots in Modesto.")
print("🐳 Powered by secure Docker environment: nicholaskarlson/pymapgis-jupyter:secure")
