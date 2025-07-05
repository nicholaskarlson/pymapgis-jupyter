# 🏙️ City Analysis Templates

This guide provides ready-to-use templates for common spatial analysis scenarios. Each template includes pre-configured parameters and code snippets that you can adapt for your specific city.

## 📋 Template Categories

### 🌆 Urban Analysis Templates
- **[Metropolitan Area Analysis](#metropolitan-area-analysis)** - Large cities with multiple districts
- **[Small City Analysis](#small-city-analysis)** - Towns and smaller urban areas
- **[Suburban Analysis](#suburban-analysis)** - Suburban and residential areas

### 🎯 Use Case Templates
- **[Crime Hotspot Analysis](#crime-hotspot-analysis)** - Public safety applications
- **[Business Location Analysis](#business-location-analysis)** - Commercial clustering
- **[Transportation Hub Analysis](#transportation-hub-analysis)** - Transit and mobility
- **[Emergency Services Analysis](#emergency-services-analysis)** - Response optimization

## 🌆 Metropolitan Area Analysis

### Template: Large City (Population > 500k)

**Recommended Parameters:**
- **DBSCAN eps**: 750-1500 meters
- **min_samples**: 8-15 points
- **Hotspot spread**: 0.003-0.005 degrees
- **Noise extent**: ±0.15 degrees

```python
# Metropolitan Area Template
CITY_NAME = "Your Metro Area"
DOWNTOWN_LAT = 40.7128  # Replace with your coordinates
DOWNTOWN_LON = -74.0060
UTM_EPSG = 32618  # Replace with correct UTM zone

# Large city parameters
DBSCAN_EPS = 1000  # 1km radius for clusters
MIN_SAMPLES = 10   # Higher threshold for dense urban areas
HOTSPOT_SPREAD = 0.004  # ~400m spread
NOISE_EXTENT = 0.2  # ±20km noise distribution

# Multiple hotspots for large cities
locations = {
    'downtown': (DOWNTOWN_LAT, DOWNTOWN_LON),
    'financial_district': (DOWNTOWN_LAT + 0.01, DOWNTOWN_LON + 0.01),
    'airport': (DOWNTOWN_LAT - 0.05, DOWNTOWN_LON + 0.08),
    'university': (DOWNTOWN_LAT + 0.03, DOWNTOWN_LON - 0.02),
    'shopping_center': (DOWNTOWN_LAT - 0.02, DOWNTOWN_LON - 0.03),
    'industrial_area': (DOWNTOWN_LAT + 0.08, DOWNTOWN_LON + 0.05)
}

# Generate more points for metropolitan areas
hotspot_sizes = {
    'downtown': 80,
    'financial_district': 60,
    'airport': 45,
    'university': 35,
    'shopping_center': 40,
    'industrial_area': 30
}
```

### Example Cities Using This Template
- New York City, NY
- Los Angeles, CA
- Chicago, IL
- Houston, TX
- Phoenix, AZ

## 🏘️ Small City Analysis

### Template: Small to Medium City (Population 50k-500k)

**Recommended Parameters:**
- **DBSCAN eps**: 300-750 meters
- **min_samples**: 4-8 points
- **Hotspot spread**: 0.001-0.003 degrees
- **Noise extent**: ±0.08 degrees

```python
# Small City Template
CITY_NAME = "Your Small City"
DOWNTOWN_LAT = 39.7391  # Example: Dayton, OH
DOWNTOWN_LON = -84.1938
UTM_EPSG = 32617

# Small city parameters
DBSCAN_EPS = 500   # 500m radius
MIN_SAMPLES = 5    # Lower threshold for smaller populations
HOTSPOT_SPREAD = 0.002  # ~200m spread
NOISE_EXTENT = 0.1  # ±10km noise distribution

# Fewer, more focused hotspots
locations = {
    'downtown': (DOWNTOWN_LAT, DOWNTOWN_LON),
    'main_shopping': (DOWNTOWN_LAT + 0.015, DOWNTOWN_LON - 0.01),
    'university_college': (DOWNTOWN_LAT - 0.02, DOWNTOWN_LON + 0.025),
    'residential_north': (DOWNTOWN_LAT + 0.03, DOWNTOWN_LON + 0.01)
}

# Smaller hotspot sizes
hotspot_sizes = {
    'downtown': 35,
    'main_shopping': 25,
    'university_college': 20,
    'residential_north': 15
}
```

### Example Cities Using This Template
- Modesto, CA
- Tulsa, OK
- Little Rock, AR
- Spokane, WA
- Dayton, OH

## 🏡 Suburban Analysis

### Template: Suburban/Residential Areas

**Recommended Parameters:**
- **DBSCAN eps**: 200-500 meters
- **min_samples**: 3-6 points
- **Hotspot spread**: 0.001-0.002 degrees
- **Noise extent**: ±0.05 degrees

```python
# Suburban Template
CITY_NAME = "Your Suburban Area"
CENTER_LAT = 40.0583  # Example: suburban area
CENTER_LON = -74.4057
UTM_EPSG = 32618

# Suburban parameters
DBSCAN_EPS = 300   # 300m radius for neighborhood clusters
MIN_SAMPLES = 4    # Small neighborhood groups
HOTSPOT_SPREAD = 0.0015  # ~150m spread
NOISE_EXTENT = 0.06  # ±6km noise distribution

# Suburban focal points
locations = {
    'town_center': (CENTER_LAT, CENTER_LON),
    'shopping_plaza': (CENTER_LAT + 0.01, CENTER_LON - 0.015),
    'school_district': (CENTER_LAT - 0.008, CENTER_LON + 0.012),
    'recreation_center': (CENTER_LAT + 0.005, CENTER_LON + 0.008)
}

# Smaller, more dispersed clusters
hotspot_sizes = {
    'town_center': 20,
    'shopping_plaza': 15,
    'school_district': 18,
    'recreation_center': 12
}
```

## 🚨 Crime Hotspot Analysis

### Template: Public Safety Applications

```python
# Crime Analysis Template
ANALYSIS_TYPE = "Crime Hotspot Analysis"
INCIDENT_TYPES = ['theft', 'vandalism', 'assault', 'burglary']

# Crime-specific parameters
DBSCAN_EPS = 400   # 400m radius for crime clusters
MIN_SAMPLES = 6    # Minimum incidents to form hotspot
TIME_PERIOD = "2024"  # Analysis period

# Crime hotspot locations (typically correlate with activity centers)
crime_locations = {
    'entertainment_district': (CENTER_LAT, CENTER_LON),
    'transit_station': (CENTER_LAT + 0.01, CENTER_LON - 0.01),
    'shopping_area': (CENTER_LAT - 0.005, CENTER_LON + 0.015),
    'parking_lots': (CENTER_LAT + 0.008, CENTER_LON + 0.008)
}

# Generate incidents with temporal patterns
def generate_crime_data(location, base_incidents, time_factor=1.0):
    """Generate crime incidents with realistic temporal distribution."""
    incidents = []
    for _ in range(int(base_incidents * time_factor)):
        # Add slight temporal clustering (e.g., weekend vs weekday)
        lat_offset = np.random.normal(0, HOTSPOT_SPREAD)
        lon_offset = np.random.normal(0, HOTSPOT_SPREAD)
        
        incident = Point(
            location[1] + lon_offset,
            location[0] + lat_offset
        )
        incidents.append(incident)
    return incidents
```

## 🏢 Business Location Analysis

### Template: Commercial Clustering

```python
# Business Analysis Template
ANALYSIS_TYPE = "Business Location Analysis"
BUSINESS_TYPES = ['retail', 'restaurant', 'service', 'office']

# Business clustering parameters
DBSCAN_EPS = 250   # 250m radius for business districts
MIN_SAMPLES = 8    # Minimum businesses for commercial cluster

# Commercial zones
business_locations = {
    'main_street': (CENTER_LAT, CENTER_LON),
    'strip_mall': (CENTER_LAT + 0.02, CENTER_LON - 0.01),
    'business_park': (CENTER_LAT - 0.015, CENTER_LON + 0.025),
    'downtown_core': (CENTER_LAT + 0.005, CENTER_LON - 0.005)
}

# Business density by zone type
business_density = {
    'main_street': 45,      # High density traditional main street
    'strip_mall': 25,       # Medium density suburban retail
    'business_park': 30,    # Office and service businesses
    'downtown_core': 60     # Highest density urban core
}
```

## 🚌 Transportation Hub Analysis

### Template: Transit and Mobility

```python
# Transportation Analysis Template
ANALYSIS_TYPE = "Transportation Hub Analysis"
TRANSPORT_MODES = ['bus', 'rail', 'airport', 'parking']

# Transportation-specific parameters
DBSCAN_EPS = 600   # 600m radius around transit hubs
MIN_SAMPLES = 5    # Minimum activity for transit cluster

# Transportation hubs
transport_locations = {
    'central_station': (CENTER_LAT, CENTER_LON),
    'airport': (CENTER_LAT - 0.08, CENTER_LON + 0.12),
    'bus_terminal': (CENTER_LAT + 0.01, CENTER_LON - 0.008),
    'park_and_ride': (CENTER_LAT + 0.03, CENTER_LON + 0.02),
    'metro_stops': [
        (CENTER_LAT + 0.015, CENTER_LON + 0.01),
        (CENTER_LAT - 0.01, CENTER_LON - 0.015),
        (CENTER_LAT + 0.005, CENTER_LON + 0.02)
    ]
}

# Activity levels by transport type
transport_activity = {
    'central_station': 80,
    'airport': 120,
    'bus_terminal': 40,
    'park_and_ride': 35
}
```

## 🚑 Emergency Services Analysis

### Template: Response Optimization

```python
# Emergency Services Template
ANALYSIS_TYPE = "Emergency Response Analysis"
SERVICE_TYPES = ['fire', 'medical', 'police', 'rescue']

# Emergency response parameters
DBSCAN_EPS = 800   # 800m radius for emergency clusters
MIN_SAMPLES = 4    # Minimum incidents for response planning

# High-risk areas for emergency services
emergency_locations = {
    'hospital_district': (CENTER_LAT, CENTER_LON),
    'industrial_zone': (CENTER_LAT + 0.04, CENTER_LON - 0.03),
    'elderly_housing': (CENTER_LAT - 0.02, CENTER_LON + 0.02),
    'highway_corridor': (CENTER_LAT + 0.01, CENTER_LON + 0.05),
    'dense_residential': (CENTER_LAT - 0.015, CENTER_LON - 0.02)
}

# Emergency incident frequencies
emergency_frequency = {
    'hospital_district': 60,    # High medical emergency frequency
    'industrial_zone': 25,      # Industrial accidents
    'elderly_housing': 40,      # Medical emergencies
    'highway_corridor': 35,     # Traffic incidents
    'dense_residential': 30     # General emergencies
}
```

## 🛠️ Customization Guidelines

### Adapting Templates for Your City

1. **Update Geographic Parameters**
   ```python
   # Replace with your city's coordinates
   CITY_LAT = your_latitude
   CITY_LON = your_longitude
   UTM_EPSG = your_utm_zone
   ```

2. **Adjust Clustering Parameters**
   ```python
   # Scale based on city size and density
   DBSCAN_EPS = appropriate_distance_meters
   MIN_SAMPLES = appropriate_minimum_points
   ```

3. **Modify Location Names**
   ```python
   # Use actual landmark names from your city
   locations = {
       'your_downtown': (lat, lon),
       'your_airport': (lat, lon),
       'your_university': (lat, lon)
   }
   ```

4. **Customize Visualization**
   ```python
   # Update map title and descriptions
   title = f"Spatial Analysis of {YOUR_CITY_NAME}"
   description = f"Analysis of spatial patterns in {YOUR_CITY_NAME}"
   ```

## 📊 Parameter Selection Guide

### Choosing DBSCAN Parameters

| City Size | Population | eps (meters) | min_samples | Hotspot Spread |
|-----------|------------|--------------|-------------|----------------|
| Small Town | <50k | 200-400 | 3-5 | 0.001-0.002 |
| Small City | 50k-200k | 300-600 | 4-7 | 0.002-0.003 |
| Medium City | 200k-500k | 500-800 | 6-10 | 0.003-0.004 |
| Large City | 500k-1M | 750-1200 | 8-12 | 0.004-0.005 |
| Metro Area | >1M | 1000-2000 | 10-20 | 0.005-0.008 |

### UTM Zone Reference

| Longitude Range | UTM Zone | EPSG Code (North) |
|----------------|----------|-------------------|
| -180° to -174° | 1 | 32601 |
| -174° to -168° | 2 | 32602 |
| ... | ... | ... |
| -84° to -78° | 17 | 32617 |
| -78° to -72° | 18 | 32618 |
| -72° to -66° | 19 | 32619 |

*Use the [UTM Zone Calculator](https://www.dmap.co.uk/utmworld.htm) for precise zone determination.*

## 🚀 Next Steps

1. **Choose the appropriate template** for your city size and analysis type
2. **Customize the parameters** using the guidelines above
3. **Test with your data** and adjust parameters as needed
4. **Enhance visualizations** with city-specific styling
5. **Share your results** with the community

## 📚 Related Documentation

- **[Creating Custom Notebooks](creating-notebooks.md)** - Detailed step-by-step guide
- **[Data Import Guide](data-import.md)** - Working with real datasets
- **[Visualization Guide](visualization-guide.md)** - Advanced mapping techniques

---

*These templates provide a starting point for your analysis. Adapt them based on your specific requirements and local geographic characteristics.*
