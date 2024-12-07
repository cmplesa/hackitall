import rasterio
from rasterio.windows import from_bounds
from pyproj import Proj
import numpy as np

# Path to your GHS-POP GeoTIFF file
ghs_pop_path = "GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0_R4_C21.tif"

# (top-left, top-right, bottom-right, bottom-left)
coordinates = [
    (44.435, 26.098),  # Top-left
    (44.435, 26.118),  # Top-right
    (44.415, 26.118),  # Bottom-right
    (44.415, 26.098)   # Bottom-left
]

# Open the raster file
with rasterio.open(ghs_pop_path) as dataset:
    # Check the CRS of the raster
    raster_crs = dataset.crs
    print(f"Raster CRS: {raster_crs}")
    
    # Convert coordinates to raster CRS
    project = Proj(raster_crs)
    transformed_coords = [project(lon, lat) for lat, lon in coordinates]
    
    # Get the bounding box in raster CRS
    x_coords, y_coords = zip(*transformed_coords)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Create a window using the bounding box
    window = from_bounds(min_x, min_y, max_x, max_y, dataset.transform)
    
    # Read the population data within the window
    population_data = dataset.read(1, window=window)
    
    # Calculate block areas (assuming resolution is 100m x 100m)
    block_area_km2 = (100 / 1000) * (100 / 1000)  # Convert to square kilometers
    
    # Calculate total area of the big region
    big_area_km2 = population_data.shape[0] * population_data.shape[1] * block_area_km2

# Print results
print(f"Big area (km²): {big_area_km2:.2f}")
print(f"Small block area (km²): {block_area_km2:.6f}")
print("Population matrix:")
print(population_data)