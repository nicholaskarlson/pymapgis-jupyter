# 🗺️ Basic Spatial Analysis Examples

This document provides fundamental examples of spatial analysis workflows using the PyMapGIS Jupyter environment.

## 🎯 Overview

These examples demonstrate core spatial analysis concepts:
- **Point pattern analysis** - Understanding spatial distributions
- **Distance calculations** - Measuring spatial relationships
- **Buffer operations** - Creating zones of influence
- **Spatial joins** - Combining datasets based on location
- **Basic clustering** - Identifying spatial groups

## 📍 Point Pattern Analysis

### Creating and Analyzing Point Patterns
```python
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Generate random point pattern
np.random.seed(42)
n_points = 100

# Random distribution
random_points = [
    Point(np.random.uniform(-1, 1), np.random.uniform(-1, 1)) 
    for _ in range(n_points)
]

# Clustered distribution
cluster_centers = [(0.3, 0.3), (-0.4, 0.2), (0.1, -0.5)]
clustered_points = []
for center in cluster_centers:
    for _ in range(30):
        x = np.random.normal(center[0], 0.1)
        y = np.random.normal(center[1], 0.1)
        clustered_points.append(Point(x, y))

# Create GeoDataFrames
random_gdf = gpd.GeoDataFrame({'type': 'random'}, geometry=random_points, crs='EPSG:4326')
clustered_gdf = gpd.GeoDataFrame({'type': 'clustered'}, geometry=clustered_points, crs='EPSG:4326')

# Visualize patterns
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

random_gdf.plot(ax=ax1, color='blue', alpha=0.6, markersize=20)
ax1.set_title('Random Point Pattern')
ax1.set_aspect('equal')

clustered_gdf.plot(ax=ax2, color='red', alpha=0.6, markersize=20)
ax2.set_title('Clustered Point Pattern')
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()
```

### Nearest Neighbor Analysis
```python
from sklearn.neighbors import NearestNeighbors

def nearest_neighbor_analysis(gdf):
    """Calculate nearest neighbor statistics."""
    
    # Extract coordinates
    coords = np.array([[point.x, point.y] for point in gdf.geometry])
    
    # Find nearest neighbors
    nbrs = NearestNeighbors(n_neighbors=2).fit(coords)
    distances, indices = nbrs.kneighbors(coords)
    
    # Get distances to nearest neighbor (excluding self)
    nn_distances = distances[:, 1]
    
    # Calculate statistics
    mean_distance = np.mean(nn_distances)
    std_distance = np.std(nn_distances)
    
    # Expected distance for random pattern
    area = (gdf.total_bounds[2] - gdf.total_bounds[0]) * (gdf.total_bounds[3] - gdf.total_bounds[1])
    density = len(gdf) / area
    expected_distance = 1 / (2 * np.sqrt(density))
    
    # Nearest neighbor ratio
    nn_ratio = mean_distance / expected_distance
    
    return {
        'mean_distance': mean_distance,
        'std_distance': std_distance,
        'expected_distance': expected_distance,
        'nn_ratio': nn_ratio,
        'pattern_type': 'clustered' if nn_ratio < 1 else 'dispersed' if nn_ratio > 1 else 'random'
    }

# Analyze both patterns
random_stats = nearest_neighbor_analysis(random_gdf)
clustered_stats = nearest_neighbor_analysis(clustered_gdf)

print("Random Pattern Analysis:")
print(f"  Mean NN Distance: {random_stats['mean_distance']:.4f}")
print(f"  NN Ratio: {random_stats['nn_ratio']:.4f} ({random_stats['pattern_type']})")

print("\nClustered Pattern Analysis:")
print(f"  Mean NN Distance: {clustered_stats['mean_distance']:.4f}")
print(f"  NN Ratio: {clustered_stats['nn_ratio']:.4f} ({clustered_stats['pattern_type']})")
```

## 📏 Distance Calculations

### Point-to-Point Distances
```python
from scipy.spatial.distance import pdist, squareform

def calculate_distance_matrix(gdf):
    """Calculate distance matrix between all points."""
    
    # Project to UTM for accurate distances
    # Determine UTM zone from center longitude
    center_lon = gdf.geometry.centroid.x.mean()
    utm_zone = int((center_lon + 180) / 6) + 1
    utm_epsg = 32600 + utm_zone  # Northern hemisphere
    
    gdf_utm = gdf.to_crs(f'EPSG:{utm_epsg}')
    
    # Extract coordinates
    coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])
    
    # Calculate pairwise distances
    distances = pdist(coords, metric='euclidean')
    distance_matrix = squareform(distances)
    
    return distance_matrix, gdf_utm

# Calculate distances for clustered pattern
dist_matrix, clustered_utm = calculate_distance_matrix(clustered_gdf)

# Find closest and farthest pairs
min_distance = np.min(dist_matrix[dist_matrix > 0])  # Exclude self-distances
max_distance = np.max(dist_matrix)

print(f"Minimum distance between points: {min_distance:.2f} meters")
print(f"Maximum distance between points: {max_distance:.2f} meters")
print(f"Average distance between points: {np.mean(dist_matrix[dist_matrix > 0]):.2f} meters")
```

### Distance to Features
```python
def distance_to_nearest_feature(points_gdf, features_gdf):
    """Calculate distance from each point to nearest feature."""
    
    # Ensure same CRS
    if points_gdf.crs != features_gdf.crs:
        features_gdf = features_gdf.to_crs(points_gdf.crs)
    
    distances = []
    for point in points_gdf.geometry:
        # Calculate distance to all features
        point_distances = features_gdf.geometry.distance(point)
        min_distance = point_distances.min()
        distances.append(min_distance)
    
    return distances

# Example: Create some "facilities" and calculate distances
facility_locations = [Point(0, 0), Point(0.5, 0.5), Point(-0.3, 0.4)]
facilities_gdf = gpd.GeoDataFrame({'type': 'facility'}, geometry=facility_locations, crs='EPSG:4326')

# Calculate distances from clustered points to facilities
distances_to_facilities = distance_to_nearest_feature(clustered_gdf, facilities_gdf)
clustered_gdf['distance_to_facility'] = distances_to_facilities

# Visualize
fig, ax = plt.subplots(figsize=(10, 8))

# Plot points colored by distance to facility
clustered_gdf.plot(column='distance_to_facility', cmap='viridis', ax=ax, 
                   legend=True, markersize=50, alpha=0.7)

# Plot facilities
facilities_gdf.plot(ax=ax, color='red', markersize=200, marker='s', alpha=0.8)

ax.set_title('Distance to Nearest Facility')
plt.show()
```

## 🔵 Buffer Operations

### Creating Buffers
```python
def create_buffers(gdf, buffer_distance, units='meters'):
    """Create buffers around geometries."""
    
    if units == 'meters':
        # Project to UTM for meter-based buffers
        center_lon = gdf.geometry.centroid.x.mean()
        utm_zone = int((center_lon + 180) / 6) + 1
        utm_epsg = 32600 + utm_zone
        
        gdf_utm = gdf.to_crs(f'EPSG:{utm_epsg}')
        buffered_utm = gdf_utm.copy()
        buffered_utm['geometry'] = gdf_utm.geometry.buffer(buffer_distance)
        
        # Convert back to original CRS
        buffered = buffered_utm.to_crs(gdf.crs)
    else:
        # Use degree-based buffers (less accurate)
        buffered = gdf.copy()
        buffered['geometry'] = gdf.geometry.buffer(buffer_distance)
    
    return buffered

# Create buffers around facilities
facility_buffers = create_buffers(facilities_gdf, 500)  # 500 meter buffers

# Visualize buffers
fig, ax = plt.subplots(figsize=(10, 8))

# Plot buffers
facility_buffers.plot(ax=ax, color='lightblue', alpha=0.5, edgecolor='blue')

# Plot original facilities
facilities_gdf.plot(ax=ax, color='red', markersize=100, marker='s')

# Plot points
clustered_gdf.plot(ax=ax, color='black', markersize=20, alpha=0.7)

ax.set_title('500m Buffers Around Facilities')
ax.set_aspect('equal')
plt.show()
```

### Buffer Analysis
```python
def points_in_buffers(points_gdf, buffer_gdf):
    """Find points within buffers."""
    
    # Spatial join to find points within buffers
    points_in_buffer = gpd.sjoin(points_gdf, buffer_gdf, how='inner', predicate='within')
    
    # Count points per buffer
    buffer_counts = points_in_buffer.groupby('index_right').size()
    
    return points_in_buffer, buffer_counts

# Analyze points within facility buffers
points_in_buffers, buffer_counts = points_in_buffers(clustered_gdf, facility_buffers)

print("Points within facility buffers:")
for i, count in buffer_counts.items():
    print(f"  Facility {i}: {count} points")

# Calculate coverage
total_points = len(clustered_gdf)
covered_points = len(points_in_buffers)
coverage_percentage = (covered_points / total_points) * 100

print(f"\nCoverage Analysis:")
print(f"  Total points: {total_points}")
print(f"  Points within 500m of facilities: {covered_points}")
print(f"  Coverage percentage: {coverage_percentage:.1f}%")
```

## 🔗 Spatial Joins

### Point-in-Polygon Analysis
```python
from shapely.geometry import Polygon

# Create some polygonal regions
regions = [
    Polygon([(-0.8, -0.8), (-0.8, 0.2), (-0.2, 0.2), (-0.2, -0.8)]),  # Region A
    Polygon([(-0.2, -0.2), (-0.2, 0.8), (0.8, 0.8), (0.8, -0.2)]),    # Region B
    Polygon([(-0.5, 0.2), (-0.5, 0.8), (0.3, 0.8), (0.3, 0.2)])       # Region C
]

regions_gdf = gpd.GeoDataFrame({
    'region_id': ['A', 'B', 'C'],
    'region_name': ['Southwest', 'Northeast', 'North Central']
}, geometry=regions, crs='EPSG:4326')

# Spatial join: assign points to regions
points_with_regions = gpd.sjoin(clustered_gdf, regions_gdf, how='left', predicate='within')

# Count points per region
region_counts = points_with_regions['region_id'].value_counts()

print("Points per region:")
for region, count in region_counts.items():
    print(f"  Region {region}: {count} points")

# Visualize
fig, ax = plt.subplots(figsize=(10, 8))

# Plot regions
regions_gdf.plot(ax=ax, alpha=0.3, edgecolor='black', linewidth=2)

# Plot points colored by region
points_with_regions.plot(column='region_id', ax=ax, legend=True, 
                        markersize=50, alpha=0.8)

# Add region labels
for idx, row in regions_gdf.iterrows():
    centroid = row.geometry.centroid
    ax.annotate(f"Region {row['region_id']}", 
                xy=(centroid.x, centroid.y), 
                ha='center', va='center', 
                fontsize=12, fontweight='bold')

ax.set_title('Points Assigned to Regions')
ax.set_aspect('equal')
plt.show()
```

### Proximity Analysis
```python
def proximity_analysis(points_gdf, features_gdf, distance_threshold):
    """Analyze proximity between points and features."""
    
    # Create buffers around features
    feature_buffers = create_buffers(features_gdf, distance_threshold)
    
    # Find points within proximity
    nearby_points = gpd.sjoin(points_gdf, feature_buffers, how='inner', predicate='within')
    
    # Calculate actual distances
    distances = []
    for idx, point_row in nearby_points.iterrows():
        point_geom = point_row.geometry
        feature_idx = point_row['index_right']
        feature_geom = features_gdf.iloc[feature_idx].geometry
        
        # Calculate distance (convert to meters if needed)
        if points_gdf.crs.to_string() == 'EPSG:4326':
            # Approximate conversion for small distances
            distance = point_geom.distance(feature_geom) * 111000  # degrees to meters
        else:
            distance = point_geom.distance(feature_geom)
        
        distances.append(distance)
    
    nearby_points['distance_to_feature'] = distances
    
    return nearby_points

# Analyze proximity to facilities (within 300m)
nearby_analysis = proximity_analysis(clustered_gdf, facilities_gdf, 300)

print(f"Points within 300m of facilities: {len(nearby_analysis)}")
print(f"Average distance to nearest facility: {nearby_analysis['distance_to_feature'].mean():.1f}m")
print(f"Minimum distance to facility: {nearby_analysis['distance_to_feature'].min():.1f}m")
print(f"Maximum distance to facility: {nearby_analysis['distance_to_feature'].max():.1f}m")
```

## 🎯 Basic Clustering

### K-Means Clustering
```python
from sklearn.cluster import KMeans

def kmeans_spatial_clustering(gdf, n_clusters=3):
    """Apply K-means clustering to spatial data."""
    
    # Extract coordinates
    coords = np.array([[point.x, point.y] for point in gdf.geometry])
    
    # Apply K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(coords)
    
    # Add cluster labels to GeoDataFrame
    gdf_clustered = gdf.copy()
    gdf_clustered['kmeans_cluster'] = cluster_labels
    
    # Get cluster centers
    cluster_centers = [Point(center[0], center[1]) for center in kmeans.cluster_centers_]
    centers_gdf = gpd.GeoDataFrame({
        'cluster_id': range(n_clusters),
        'geometry': cluster_centers
    }, crs=gdf.crs)
    
    return gdf_clustered, centers_gdf

# Apply K-means clustering
clustered_kmeans, cluster_centers = kmeans_spatial_clustering(clustered_gdf, n_clusters=3)

# Visualize K-means results
fig, ax = plt.subplots(figsize=(10, 8))

# Plot points colored by cluster
clustered_kmeans.plot(column='kmeans_cluster', cmap='viridis', ax=ax, 
                     legend=True, markersize=50, alpha=0.7)

# Plot cluster centers
cluster_centers.plot(ax=ax, color='red', markersize=200, marker='X', 
                    edgecolor='black', linewidth=2)

ax.set_title('K-Means Spatial Clustering')
ax.set_aspect('equal')
plt.show()

# Cluster statistics
for cluster_id in clustered_kmeans['kmeans_cluster'].unique():
    cluster_points = clustered_kmeans[clustered_kmeans['kmeans_cluster'] == cluster_id]
    print(f"Cluster {cluster_id}: {len(cluster_points)} points")
```

### Hierarchical Clustering
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

def hierarchical_clustering(gdf, n_clusters=3, linkage_method='ward'):
    """Apply hierarchical clustering to spatial data."""
    
    # Extract coordinates
    coords = np.array([[point.x, point.y] for point in gdf.geometry])
    
    # Apply hierarchical clustering
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method)
    cluster_labels = hierarchical.fit_predict(coords)
    
    # Add cluster labels
    gdf_clustered = gdf.copy()
    gdf_clustered['hierarchical_cluster'] = cluster_labels
    
    # Create linkage matrix for dendrogram
    linkage_matrix = linkage(coords, method=linkage_method)
    
    return gdf_clustered, linkage_matrix

# Apply hierarchical clustering
clustered_hierarchical, linkage_matrix = hierarchical_clustering(clustered_gdf, n_clusters=3)

# Visualize results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot spatial clusters
clustered_hierarchical.plot(column='hierarchical_cluster', cmap='Set1', ax=ax1, 
                           legend=True, markersize=50, alpha=0.7)
ax1.set_title('Hierarchical Spatial Clustering')
ax1.set_aspect('equal')

# Plot dendrogram
dendrogram(linkage_matrix, ax=ax2, truncate_mode='level', p=5)
ax2.set_title('Clustering Dendrogram')
ax2.set_xlabel('Sample Index')
ax2.set_ylabel('Distance')

plt.tight_layout()
plt.show()
```

## 📊 Analysis Summary

### Comprehensive Spatial Analysis Report
```python
def spatial_analysis_report(gdf, analysis_name="Spatial Analysis"):
    """Generate comprehensive spatial analysis report."""
    
    print(f"=== {analysis_name.upper()} REPORT ===")
    print(f"Dataset: {len(gdf)} points")
    print(f"CRS: {gdf.crs}")
    
    # Spatial extent
    bounds = gdf.total_bounds
    print(f"\nSpatial Extent:")
    print(f"  Min X: {bounds[0]:.6f}")
    print(f"  Min Y: {bounds[1]:.6f}")
    print(f"  Max X: {bounds[2]:.6f}")
    print(f"  Max Y: {bounds[3]:.6f}")
    print(f"  Width: {bounds[2] - bounds[0]:.6f}")
    print(f"  Height: {bounds[3] - bounds[1]:.6f}")
    
    # Centroid
    centroid = gdf.geometry.unary_union.centroid
    print(f"\nCentroid: ({centroid.x:.6f}, {centroid.y:.6f})")
    
    # Nearest neighbor analysis
    nn_stats = nearest_neighbor_analysis(gdf)
    print(f"\nNearest Neighbor Analysis:")
    print(f"  Mean distance: {nn_stats['mean_distance']:.6f}")
    print(f"  Standard deviation: {nn_stats['std_distance']:.6f}")
    print(f"  Expected distance (random): {nn_stats['expected_distance']:.6f}")
    print(f"  NN Ratio: {nn_stats['nn_ratio']:.3f}")
    print(f"  Pattern type: {nn_stats['pattern_type']}")
    
    # Density
    area = (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])
    density = len(gdf) / area
    print(f"\nDensity: {density:.2f} points per unit area")
    
    return nn_stats

# Generate reports for different patterns
print("RANDOM PATTERN ANALYSIS")
random_report = spatial_analysis_report(random_gdf, "Random Pattern")

print("\n" + "="*50)
print("CLUSTERED PATTERN ANALYSIS")
clustered_report = spatial_analysis_report(clustered_gdf, "Clustered Pattern")
```

## 🚀 Next Steps

After mastering these basic spatial analysis techniques:

1. **Explore advanced clustering** - Try DBSCAN, OPTICS, or custom algorithms
2. **Add temporal analysis** - Incorporate time-based patterns
3. **Work with real data** - Apply techniques to actual datasets
4. **Combine multiple analyses** - Create comprehensive spatial workflows
5. **Develop custom functions** - Build reusable analysis tools

## 📚 Related Documentation

- **[Advanced Clustering Examples](advanced-clustering.md)** - More sophisticated clustering techniques
- **[Multi-City Analysis](multi-city-analysis.md)** - Comparative spatial analysis
- **[Creating Custom Notebooks](../user-guides/creating-notebooks.md)** - Building complete analysis workflows

---

*These examples provide the foundation for spatial analysis. Combine and extend them to create powerful analytical workflows for your specific use cases.*
