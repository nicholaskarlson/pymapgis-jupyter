# 🎨 Visualization Guide

This guide covers advanced visualization techniques for spatial data analysis in the PyMapGIS Jupyter environment, from basic maps to sophisticated interactive visualizations.

## 🎯 Overview

The PyMapGIS environment provides multiple visualization libraries:
- **Folium** - Interactive web maps
- **Matplotlib/GeoPandas** - Static publication-quality maps
- **Plotly** - Interactive charts and 3D visualizations
- **Seaborn** - Statistical visualizations
- **Contextily** - Basemap integration

## 🗺️ Interactive Maps with Folium

### Basic Interactive Map
```python
import folium
import geopandas as gpd

# Create base map
center_lat, center_lon = gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles='OpenStreetMap'
)

# Add points with popups
for idx, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=8,
        popup=f"ID: {row['id']}<br>Value: {row['value']}",
        tooltip=f"Point {row['id']}",
        color='blue',
        fill=True,
        fillColor='lightblue',
        fillOpacity=0.7
    ).add_to(m)

m
```

### Cluster-Based Coloring
```python
# Color mapping for clusters
def get_cluster_color(cluster_id):
    """Get color for cluster ID."""
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
              'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']
    
    if cluster_id == -1:
        return 'gray'  # Noise points
    else:
        return colors[cluster_id % len(colors)]

# Create map with cluster colors
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles='CartoDB positron'
)

for idx, row in gdf.iterrows():
    cluster_id = row['cluster_id']
    color = get_cluster_color(cluster_id)
    
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=6,
        popup=f"Cluster: {cluster_id}<br>Point: {row['id']}",
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.8
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 150px; height: 90px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 10px">
<p><b>Cluster Legend</b></p>
<p><i class="fa fa-circle" style="color:red"></i> Cluster 0</p>
<p><i class="fa fa-circle" style="color:blue"></i> Cluster 1</p>
<p><i class="fa fa-circle" style="color:gray"></i> Noise</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

m
```

### Advanced Map Features
```python
# Map with multiple layers and controls
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12
)

# Add different tile layers
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('Stamen Terrain').add_to(m)

# Cluster layer
cluster_group = folium.FeatureGroup(name='Clusters')
for idx, row in gdf.iterrows():
    if row['cluster_id'] != -1:  # Only clusters, not noise
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=8,
            popup=f"Cluster {row['cluster_id']}",
            color=get_cluster_color(row['cluster_id']),
            fill=True
        ).add_to(cluster_group)

# Noise layer
noise_group = folium.FeatureGroup(name='Noise Points')
noise_data = gdf[gdf['cluster_id'] == -1]
for idx, row in noise_data.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=4,
        popup="Noise Point",
        color='gray',
        fill=True
    ).add_to(noise_group)

# Add layers to map
cluster_group.add_to(m)
noise_group.add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Add fullscreen button
from folium import plugins
plugins.Fullscreen().add_to(m)

m
```

### Heat Maps
```python
from folium.plugins import HeatMap

# Create heat map
heat_data = [[row.geometry.y, row.geometry.x] for idx, row in gdf.iterrows()]

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles='CartoDB dark_matter'
)

HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)

m
```

## 📊 Static Maps with Matplotlib

### Basic Static Map
```python
import matplotlib.pyplot as plt
import contextily as ctx

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Plot data
gdf.plot(
    column='cluster_id',
    cmap='viridis',
    ax=ax,
    legend=True,
    markersize=50,
    alpha=0.7
)

# Add basemap
gdf_web_mercator = gdf.to_crs(epsg=3857)
ctx.add_basemap(ax, crs=gdf_web_mercator.crs, source=ctx.providers.CartoDB.Positron)

# Styling
ax.set_title(f'Spatial Clusters in {CITY_NAME}', fontsize=16, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### Multi-Panel Visualization
```python
# Create subplot layout
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Panel 1: Cluster map
gdf.plot(column='cluster_id', cmap='tab10', ax=axes[0,0], legend=True, markersize=30)
axes[0,0].set_title('Spatial Clusters')

# Panel 2: Density plot
gdf_utm.plot(ax=axes[0,1], color='red', alpha=0.6, markersize=20)
axes[0,1].set_title('Point Density')

# Panel 3: Cluster size histogram
cluster_counts = gdf['cluster_id'].value_counts().sort_index()
cluster_counts.plot(kind='bar', ax=axes[1,0], color='skyblue')
axes[1,0].set_title('Cluster Sizes')
axes[1,0].set_xlabel('Cluster ID')
axes[1,0].set_ylabel('Number of Points')

# Panel 4: Distance distribution
from sklearn.neighbors import NearestNeighbors
coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])
nbrs = NearestNeighbors(n_neighbors=2).fit(coords)
distances, indices = nbrs.kneighbors(coords)
nearest_distances = distances[:, 1]  # Distance to nearest neighbor

axes[1,1].hist(nearest_distances, bins=30, alpha=0.7, color='green')
axes[1,1].set_title('Nearest Neighbor Distances')
axes[1,1].set_xlabel('Distance (meters)')
axes[1,1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
```

### Publication-Quality Maps
```python
# High-quality map for publications
fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

# Plot with custom styling
gdf.plot(
    column='cluster_id',
    cmap='Set1',
    ax=ax,
    legend=True,
    markersize=60,
    alpha=0.8,
    edgecolor='black',
    linewidth=0.5
)

# Add basemap
ctx.add_basemap(ax, crs=gdf.to_crs(epsg=3857).crs, 
                source=ctx.providers.CartoDB.Positron)

# Professional styling
ax.set_title(f'Spatial Clustering Analysis: {CITY_NAME}', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)

# Remove axis ticks for cleaner look
ax.set_xticks([])
ax.set_yticks([])

# Add north arrow and scale bar
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import Rectangle

# North arrow
arrow = FancyArrowPatch((0.9, 0.9), (0.9, 0.95),
                       connectionstyle="arc3", 
                       transform=ax.transAxes,
                       arrowstyle='->', 
                       mutation_scale=20, 
                       color='black')
ax.add_patch(arrow)
ax.text(0.92, 0.92, 'N', transform=ax.transAxes, fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{CITY_NAME.lower().replace(" ", "_")}_clusters.png', 
            dpi=300, bbox_inches='tight')
plt.show()
```

## 📈 Interactive Charts with Plotly

### 3D Scatter Plot
```python
import plotly.express as px
import plotly.graph_objects as go

# Prepare data for 3D visualization
plot_data = gdf.copy()
plot_data['x'] = plot_data.geometry.x
plot_data['y'] = plot_data.geometry.y
plot_data['z'] = plot_data['cluster_id']  # Use cluster as height

# Create 3D scatter plot
fig = px.scatter_3d(
    plot_data,
    x='x', y='y', z='z',
    color='cluster_id',
    title=f'3D Cluster Visualization: {CITY_NAME}',
    labels={'x': 'Longitude', 'y': 'Latitude', 'z': 'Cluster ID'}
)

fig.update_traces(marker_size=5)
fig.show()
```

### Interactive Dashboard
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Create subplot dashboard
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Cluster Map', 'Cluster Sizes', 'Distance Distribution', 'Summary Stats'),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "histogram"}, {"type": "table"}]]
)

# Map view
fig.add_trace(
    go.Scatter(
        x=gdf.geometry.x,
        y=gdf.geometry.y,
        mode='markers',
        marker=dict(
            color=gdf['cluster_id'],
            colorscale='viridis',
            size=8
        ),
        text=[f"Cluster: {cid}" for cid in gdf['cluster_id']],
        name='Points'
    ),
    row=1, col=1
)

# Cluster sizes
cluster_counts = gdf['cluster_id'].value_counts().sort_index()
fig.add_trace(
    go.Bar(
        x=cluster_counts.index,
        y=cluster_counts.values,
        name='Cluster Sizes'
    ),
    row=1, col=2
)

# Distance distribution
fig.add_trace(
    go.Histogram(
        x=nearest_distances,
        nbinsx=20,
        name='Distances'
    ),
    row=2, col=1
)

# Summary table
summary_data = [
    ['Total Points', len(gdf)],
    ['Number of Clusters', len(set(gdf['cluster_id'])) - (1 if -1 in gdf['cluster_id'].values else 0)],
    ['Noise Points', sum(gdf['cluster_id'] == -1)],
    ['Largest Cluster', cluster_counts.max()],
    ['Average Cluster Size', cluster_counts.mean()]
]

fig.add_trace(
    go.Table(
        header=dict(values=['Metric', 'Value']),
        cells=dict(values=list(zip(*summary_data)))
    ),
    row=2, col=2
)

fig.update_layout(height=800, title_text=f"Spatial Analysis Dashboard: {CITY_NAME}")
fig.show()
```

## 📊 Statistical Visualizations

### Cluster Analysis Plots
```python
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.figure(figsize=(15, 10))

# Subplot 1: Cluster size distribution
plt.subplot(2, 3, 1)
cluster_counts = gdf['cluster_id'].value_counts()
sns.barplot(x=cluster_counts.index, y=cluster_counts.values, palette='viridis')
plt.title('Cluster Size Distribution')
plt.xlabel('Cluster ID')
plt.ylabel('Number of Points')

# Subplot 2: Distance to cluster center
plt.subplot(2, 3, 2)
# Calculate distances to cluster centers
cluster_centers = gdf_utm.groupby('cluster_id').geometry.apply(
    lambda x: Point(x.x.mean(), x.y.mean())
)

distances_to_center = []
for idx, row in gdf_utm.iterrows():
    if row['cluster_id'] != -1:
        center = cluster_centers[row['cluster_id']]
        dist = row.geometry.distance(center)
        distances_to_center.append(dist)

plt.hist(distances_to_center, bins=20, alpha=0.7, color='orange')
plt.title('Distance to Cluster Center')
plt.xlabel('Distance (meters)')
plt.ylabel('Frequency')

# Subplot 3: Cluster compactness
plt.subplot(2, 3, 3)
cluster_compactness = []
for cluster_id in gdf_utm['cluster_id'].unique():
    if cluster_id != -1:
        cluster_points = gdf_utm[gdf_utm['cluster_id'] == cluster_id]
        center = cluster_centers[cluster_id]
        avg_distance = cluster_points.geometry.distance(center).mean()
        cluster_compactness.append(avg_distance)

plt.bar(range(len(cluster_compactness)), cluster_compactness, color='lightcoral')
plt.title('Cluster Compactness')
plt.xlabel('Cluster Index')
plt.ylabel('Average Distance to Center (m)')

# Subplot 4: Spatial autocorrelation
plt.subplot(2, 3, 4)
from scipy.spatial.distance import pdist, squareform
coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])
distances = squareform(pdist(coords))

# Plot distance vs cluster similarity
same_cluster = []
distance_pairs = []
for i in range(len(gdf)):
    for j in range(i+1, len(gdf)):
        distance_pairs.append(distances[i, j])
        same_cluster.append(1 if gdf.iloc[i]['cluster_id'] == gdf.iloc[j]['cluster_id'] else 0)

plt.scatter(distance_pairs[:1000], same_cluster[:1000], alpha=0.5)  # Sample for performance
plt.title('Spatial Autocorrelation')
plt.xlabel('Distance (meters)')
plt.ylabel('Same Cluster (1=Yes, 0=No)')

# Subplot 5: Cluster silhouette analysis
plt.subplot(2, 3, 5)
from sklearn.metrics import silhouette_samples, silhouette_score

if len(set(gdf['cluster_id'])) > 1:
    # Remove noise points for silhouette analysis
    clustered_data = gdf_utm[gdf_utm['cluster_id'] != -1]
    clustered_coords = np.array([[point.x, point.y] for point in clustered_data.geometry])
    
    if len(clustered_data) > 0:
        silhouette_avg = silhouette_score(clustered_coords, clustered_data['cluster_id'])
        sample_silhouette_values = silhouette_samples(clustered_coords, clustered_data['cluster_id'])
        
        plt.hist(sample_silhouette_values, bins=20, alpha=0.7, color='green')
        plt.axvline(silhouette_avg, color='red', linestyle='--', 
                   label=f'Average: {silhouette_avg:.3f}')
        plt.title('Silhouette Analysis')
        plt.xlabel('Silhouette Score')
        plt.ylabel('Frequency')
        plt.legend()

# Subplot 6: Geographic spread
plt.subplot(2, 3, 6)
bounds = gdf_utm.total_bounds
width = bounds[2] - bounds[0]
height = bounds[3] - bounds[1]

metrics = ['Width (km)', 'Height (km)', 'Area (km²)', 'Density (pts/km²)']
values = [width/1000, height/1000, (width*height)/1000000, len(gdf)/((width*height)/1000000)]

plt.bar(metrics, values, color='purple', alpha=0.7)
plt.title('Geographic Metrics')
plt.xticks(rotation=45)
plt.ylabel('Value')

plt.tight_layout()
plt.show()
```

## 🎨 Custom Styling and Themes

### Custom Color Palettes
```python
# Define custom color schemes
color_schemes = {
    'urban': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
    'nature': ['#6C5CE7', '#A29BFE', '#74B9FF', '#0984E3', '#00B894'],
    'professional': ['#2D3436', '#636E72', '#B2BEC3', '#DDD', '#74B9FF'],
    'vibrant': ['#E17055', '#FDCB6E', '#6C5CE7', '#A29BFE', '#FD79A8']
}

def apply_color_scheme(scheme_name='urban'):
    """Apply custom color scheme to visualizations."""
    colors = color_schemes.get(scheme_name, color_schemes['urban'])
    return colors

# Use custom colors in maps
custom_colors = apply_color_scheme('nature')

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

for idx, row in gdf.iterrows():
    cluster_id = row['cluster_id']
    if cluster_id == -1:
        color = '#95A5A6'  # Gray for noise
    else:
        color = custom_colors[cluster_id % len(custom_colors)]
    
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=7,
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.8
    ).add_to(m)

m
```

### Responsive Design
```python
# Create responsive visualizations that work on different screen sizes
def create_responsive_map(gdf, width='100%', height='500px'):
    """Create a responsive map that adapts to container size."""
    
    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        width=width,
        height=height
    )
    
    # Add responsive features
    folium.plugins.Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(m)
    
    return m

# Create maps for different contexts
mobile_map = create_responsive_map(gdf, width='100%', height='400px')
desktop_map = create_responsive_map(gdf, width='100%', height='600px')
```

## 📱 Export and Sharing

### Export Maps
```python
# Export interactive map as HTML
m.save(f'{CITY_NAME.lower().replace(" ", "_")}_interactive_map.html')

# Export static map as high-resolution image
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
gdf.plot(column='cluster_id', cmap='viridis', ax=ax, legend=True)
plt.savefig(f'{CITY_NAME.lower().replace(" ", "_")}_static_map.png', 
            dpi=300, bbox_inches='tight', facecolor='white')

# Export as PDF for publications
plt.savefig(f'{CITY_NAME.lower().replace(" ", "_")}_static_map.pdf', 
            bbox_inches='tight', facecolor='white')
```

### Create Animated Visualizations
```python
# Create animated GIF showing clustering process
import matplotlib.animation as animation

def animate_clustering(gdf_utm, eps_values):
    """Create animation showing different eps values."""
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    def update(frame):
        ax.clear()
        
        # Run DBSCAN with current eps
        coords = np.array([[point.x, point.y] for point in gdf_utm.geometry])
        dbscan = DBSCAN(eps=eps_values[frame], min_samples=5)
        labels = dbscan.fit_predict(coords)
        
        # Plot results
        gdf_temp = gdf_utm.copy()
        gdf_temp['cluster_id'] = labels
        gdf_temp.plot(column='cluster_id', cmap='viridis', ax=ax, legend=True)
        
        ax.set_title(f'DBSCAN Clustering (eps={eps_values[frame]}m)')
        ax.set_xlabel('UTM Easting')
        ax.set_ylabel('UTM Northing')
    
    # Create animation
    eps_range = np.linspace(100, 1000, 20)
    ani = animation.FuncAnimation(fig, update, frames=len(eps_range), 
                                 interval=500, repeat=True)
    
    # Save as GIF
    ani.save(f'{CITY_NAME.lower().replace(" ", "_")}_clustering_animation.gif', 
             writer='pillow', fps=2)
    
    return ani

# Create animation
# animation = animate_clustering(gdf_utm, np.linspace(200, 800, 10))
```

## 🚀 Best Practices

### Performance Optimization
```python
# For large datasets, use these optimization techniques:

# 1. Simplify geometries for display
gdf_simplified = gdf.copy()
gdf_simplified['geometry'] = gdf_simplified.geometry.simplify(tolerance=0.001)

# 2. Use clustering for point reduction
from sklearn.cluster import KMeans
coords = np.array([[point.x, point.y] for point in gdf.geometry])
kmeans = KMeans(n_clusters=100)  # Reduce to 100 representative points
cluster_centers = kmeans.fit(coords).cluster_centers_
representative_points = [Point(x, y) for x, y in cluster_centers]

# 3. Implement level-of-detail for zoom-based display
def create_lod_map(gdf, zoom_levels):
    """Create map with level-of-detail based on zoom."""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    
    # Add different detail levels
    for zoom, sample_rate in zoom_levels.items():
        if zoom <= 10:  # Low zoom - show sample
            sample_gdf = gdf.sample(frac=sample_rate)
        else:  # High zoom - show all
            sample_gdf = gdf
            
        # Add to map with zoom-based visibility
        # (Implementation depends on specific requirements)
    
    return m
```

### Accessibility
```python
# Make visualizations accessible
def create_accessible_map(gdf):
    """Create map with accessibility features."""
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='CartoDB positron'  # High contrast tiles
    )
    
    # Use colorblind-friendly palette
    colorblind_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Add descriptive popups
    for idx, row in gdf.iterrows():
        cluster_id = row['cluster_id']
        
        # Descriptive popup text
        if cluster_id == -1:
            popup_text = "Isolated point (not part of any cluster)"
            color = '#7f7f7f'
        else:
            popup_text = f"Cluster {cluster_id} - Part of group with {sum(gdf['cluster_id'] == cluster_id)} points"
            color = colorblind_colors[cluster_id % len(colorblind_colors)]
        
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=8,
            popup=popup_text,
            tooltip=f"Click for details about this point",
            color=color,
            fill=True
        ).add_to(m)
    
    return m
```

## 📚 Additional Resources

- **[Creating Custom Notebooks](creating-notebooks.md)** - Integrating visualizations into analysis workflows
- **[City Analysis Templates](city-analysis-templates.md)** - Pre-configured visualization examples
- **[Data Import Guide](data-import.md)** - Visualizing imported datasets

---

*Ready to create stunning visualizations? Start with the basic examples and gradually incorporate advanced techniques based on your specific needs.*
