import rasterio
import geopandas as gpd
from shapely.geometry import shape
import rasterio.features

def raster_to_geojson(tiff_path, output_geojson_path):
    with rasterio.open(tiff_path) as dataset:
        band1 = dataset.read(1)  # Adjust the band number based on your TIFF data specifics

    # Convert raster data to shapes
    shapes = rasterio.features.shapes(band1, transform=dataset.transform)
    geometries = [shape(geometry) for geometry, value in shapes if value > 0.1]  # Threshold can be adjusted

    # Filter out invalid geometries and create a GeoDataFrame
    valid_geometries = [geom for geom in geometries if geom.is_valid]
    gdf = gpd.GeoDataFrame({'geometry': valid_geometries})

    # Save to GeoJSON
    gdf.to_file(output_geojson_path, driver='GeoJSON')

# Usage
tif_path = 'Reprojected_Rasterized_DEM.tif'
output_geojson = 'Reprojected_Rasterized_DEM.geojson'
raster_to_geojson(tif_path, output_geojson)
