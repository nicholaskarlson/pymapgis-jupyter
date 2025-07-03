# PyMapGIS Jupyter Notebook Environment
FROM jupyter/scipy-notebook:latest

# Switch to root to install system packages
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER $NB_UID

# Install PyMapGIS and related packages
RUN pip install --no-cache-dir \
    pymapgis \
    geopandas \
    folium \
    mapclassify \
    plotly \
    seaborn \
    contextily \
    rasterio \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

# Create notebooks directory
RUN mkdir -p /home/$NB_USER/notebooks

# Copy notebook files
COPY notebooks/ /home/$NB_USER/notebooks/

# Set working directory
WORKDIR /home/$NB_USER

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Lab
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]
