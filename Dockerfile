# PyMapGIS Jupyter Notebook Environment - Security Hardened Multi-Stage Build

# Build stage
FROM python:3.11-slim-bookworm AS builder

# Security labels
LABEL org.opencontainers.image.title="PyMapGIS Jupyter Environment" \
      org.opencontainers.image.description="Secure Docker environment for PyMapGIS spatial analysis" \
      org.opencontainers.image.vendor="Nicholas Karlson" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/nicholaskarlson/pymapgis-jupyter" \
      security.scan="enabled"

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    jupyter \
    jupyterlab \
    pymapgis \
    geopandas \
    folium \
    mapclassify \
    plotly \
    seaborn \
    contextily \
    rasterio \
    pandas \
    numpy \
    matplotlib

# Runtime stage
FROM python:3.11-slim-bookworm AS runtime

# Create non-root user
RUN groupadd --gid 1000 jupyter && \
    useradd --uid 1000 --gid jupyter --shell /bin/bash --create-home jupyter

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libgdal32 \
    libproj25 \
    libgeos-c1v5 \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && apt-get autoremove -y

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Switch to non-root user
USER jupyter
WORKDIR /home/jupyter

# Create notebooks directory
RUN mkdir -p /home/jupyter/notebooks

# Copy notebook files
COPY --chown=jupyter:jupyter notebooks/ /home/jupyter/notebooks/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8888/api/status || exit 1

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Lab with security settings
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token=''", "--ServerApp.password=''"]
