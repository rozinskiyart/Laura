import geopandas as gpd
import sys

def load_geopackage(gpkg_path, layer_name=None):
    """Load a layer from a GeoPackage file."""
    try:
        gdf = gpd.read_file(gpkg_path, layer=layer_name)  # Specify the layer name if necessary
        return gdf
    except Exception as e:
        print(f"Failed to load GeoPackage: {e}")
        sys.exit(1)

def convert_to_geojson(gdf, output_path):
    """Convert a GeoDataFrame to a GeoJSON file."""
    try:
        gdf.to_file(output_path, driver='GeoJSON')
        print(f"GeoJSON saved successfully to {output_path}")
    except Exception as e:
        print(f"Failed to save GeoJSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_to_geojson.py [path_to_gpkg] [output_geojson_path]")
        sys.exit(1)

    gpkg_path = sys.argv[1]
    output_geojson_path = sys.argv[2]
    gdf = load_geopackage(gpkg_path)
    convert_to_geojson(gdf, output_geojson_path)
