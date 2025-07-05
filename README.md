# PyMapGIS Jupyter Environment

A Docker-based Jupyter notebook environment with PyMapGIS pre-installed for spatial data analysis and machine learning.

## Features

- **Jupyter Lab** with PyMapGIS and all dependencies pre-installed
- **Spatial Analysis Tools**: GeoPandas, Folium, Rasterio, Contextily
- **Machine Learning**: PyMapGIS SpatialDBSCAN and other ML algorithms
- **Visualization**: Plotly, Seaborn, Folium for interactive maps
- **Example Notebooks**: Ready-to-run spatial analysis examples

## Quick Start

### Option 1: Run from Docker Hub

```bash
docker run -p 8888:8888 nicholaskarlson/pymapgis-jupyter:latest
```

### Option 2: Build Locally

```bash
# Clone and build
git clone <repository-url>
cd pymapgis-jupyter
docker build -t pymapgis-jupyter .

# Run the container
docker run -p 8888:8888 pymapgis-jupyter
```

### Option 3: Docker Compose

```bash
docker-compose up
```

## Access

After starting the container, open your browser and navigate to:
```
http://localhost:8888
```

No token or password required - the environment is configured for easy local development.

## Included Notebooks

### 1. Spatial DBSCAN Example
- **File**: `spatial_dbscan_example.ipynb`
- **Description**: Demonstrates spatial clustering on simulated Little Rock incident data
- **Features**:
  - Data simulation for realistic spatial patterns
  - Coordinate system transformations
  - PyMapGIS SpatialDBSCAN clustering
  - Interactive Folium mapping

## Example Usage

The main example notebook shows how to:

1. **Install Dependencies** (if needed)
2. **Generate Spatial Data** - Simulated incident hotspots
3. **Apply Spatial Clustering** - Using PyMapGIS SpatialDBSCAN
4. **Visualize Results** - Interactive maps with cluster colors

```python
import pymapgis as pmg
from pymapgis.ml import SpatialDBSCAN
import geopandas as gpd

# Create spatial clusters
db = SpatialDBSCAN(eps=250, min_samples=5)
db.fit(data, geometry=geometries)

# Visualize on interactive map
gdf.explore(column="cluster_id", cmap="viridis")
```

## Installed Packages

- **PyMapGIS** - Spatial analysis and machine learning
- **GeoPandas** - Spatial data manipulation
- **Folium** - Interactive mapping
- **Plotly** - Interactive visualizations
- **Rasterio** - Raster data processing
- **Contextily** - Basemap tiles
- **Seaborn** - Statistical visualization
- **MapClassify** - Choropleth classification

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

### 🚀 Getting Started
- **[Quick Start Guide](docs/QUICK_START.md)** - Get running in 5 minutes
- **[Creating Custom Notebooks](docs/user-guides/creating-notebooks.md)** - Step-by-step notebook creation
- **[City Analysis Templates](docs/user-guides/city-analysis-templates.md)** - Ready-to-use templates for different city sizes

### 📖 User Guides
- **[Data Import Guide](docs/user-guides/data-import.md)** - Working with your own spatial datasets
- **[Visualization Guide](docs/user-guides/visualization-guide.md)** - Advanced mapping and visualization techniques

### 💡 Examples
- **[Basic Spatial Analysis](docs/examples/basic-spatial-analysis.md)** - Fundamental spatial operations and workflows

### 🔧 For Developers
- **[Complete Documentation Index](docs/README.md)** - Full documentation overview

## Development

### Adding New Notebooks

1. **Use the templates**: Start with existing city templates in `notebooks/`
2. **Follow the guide**: See [Creating Custom Notebooks](docs/user-guides/creating-notebooks.md)
3. **Place files**: Add `.ipynb` files in the `notebooks/` directory
4. **Test locally**: Mount a volume for live development:

```bash
docker run -p 8888:8888 -v $(pwd)/notebooks:/home/jovyan/notebooks pymapgis-jupyter
```

### Customizing the Environment

Edit the `Dockerfile` to add additional packages or configurations:

```dockerfile
RUN pip install --no-cache-dir your-package-here
```

## Publishing to Docker Hub

```bash
# Build and tag
docker build -t nicholaskarlson/pymapgis-jupyter:latest .

# Push to Docker Hub
docker push nicholaskarlson/pymapgis-jupyter:latest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your notebooks or improvements
4. Submit a pull request

## Support

For issues related to:
- **PyMapGIS**: Check the main PyMapGIS documentation
- **Docker Environment**: Open an issue in this repository
- **Jupyter**: Refer to Jupyter documentation

## Acknowledgments

- Built on the excellent `jupyter/scipy-notebook` base image
- Uses PyMapGIS for spatial machine learning capabilities
- Inspired by the need for easy-to-use spatial analysis environments
