import streamlit as st
import pandas as pd
import pydeck as pdk
import rasterio
import geopandas as gpd
from shapely.geometry import mapping
import rasterio.features
from shapely.geometry import shape
import json

# Load your data

def load_data():
    data = pd.read_csv('Transformed_Soil_Erosion_Data.csv')
    
    # Initialize columns for color and size
    data['color'] = [[0, 0, 0] for _ in range(len(data))]  # default color - black for no erosion
    data['size'] = [50 for _ in range(len(data))]  # default size - smallest size for no erosion

    # Conditional updates for color and size based on erosion rates
    data.loc[data['Erosion_Rate'] > 0, 'color'] = data.loc[data['Erosion_Rate'] > 0, 'color'].apply(lambda x: [255, 255, 179])  # Light yellow
    data.loc[data['Erosion_Rate'] > 1, 'color'] = data.loc[data['Erosion_Rate'] > 1, 'color'].apply(lambda x: [141, 211, 199])  # Teal
    data.loc[data['Erosion_Rate'] > 10, 'color'] = data.loc[data['Erosion_Rate'] > 10, 'color'].apply(lambda x: [190, 186, 218])  # Light purple
    data.loc[data['Erosion_Rate'] > 100, 'color'] = data.loc[data['Erosion_Rate'] > 100, 'color'].apply(lambda x: [251, 128, 114])  # Salmon

    data.loc[data['Erosion_Rate'] > 0, 'size'] = 500
    data.loc[data['Erosion_Rate'] > 1, 'size'] = 1000
    data.loc[data['Erosion_Rate'] > 10, 'size'] = 2000
    data.loc[data['Erosion_Rate'] > 100, 'size'] = 5000

    return data



@st.cache_data
def load_geojson(geojson_path):
    
    return gpd.read_file(geojson_path)


def load_geopackage(gpkg_path):

    return gpd.read_file(gpkg_path)
    

def process_rainfall(station_file):
    # Load data
    df = pd.read_csv(station_file)
    # Assume you calculate the average or total rainfall here
    average_rainfall = df['value'].mean()
    return average_rainfall

# bounds = load_raster_data()

df = load_data()

# Streamlit page setup
st.title('Soil Erosion Data Visualization')

# Legend display using markdown for colors
st.sidebar.title('Erosion Legend')
st.sidebar.markdown("""
- **No erosion detected**: <span style='height: 15px; width: 15px; background-color: #000000; border-radius: 50%; display: inline-block;'></span> 
- **0.01 - 1.00**: <span style='height: 15px; width: 15px; background-color: #ffffb3; border-radius: 50%; display: inline-block;'></span> 
- **1.01 - 10.00**: <span style='height: 15px; width: 15px; background-color: #8dd3c7; border-radius: 50%; display: inline-block;'></span> 
- **10.01 - 100.00**: <span style='height: 15px; width: 15px; background-color: #bebada; border-radius: 50%; display: inline-block;'></span> 
- **>100.00**: <span style='height: 15px; width: 15px; background-color: #fb8072; border-radius: 50%; display: inline-block;'></span> 
""", unsafe_allow_html=True)
st.sidebar.title('Layers Legend')
st.sidebar.markdown("""
- **Landcover**: <span style='height: 15px; width: 15px; background-color: #000000; border-radius: 50%; display: inline-block;'></span> 
- **Rainfall**: <span style='height: 15px; width: 15px; background-color: blue; border-radius: 50%; display: inline-block;'></span> 
""", unsafe_allow_html=True)
st.sidebar.title('Layers')
# Map setup
view_state = pdk.ViewState(latitude=df['latitude'].mean(), longitude=df['longitude'].mean(), zoom=6)

# Adding layers based on checkboxes

erosion_layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position=['longitude', 'latitude'],
    get_color='color',
    get_radius='size',
    pickable=True
)

if st.sidebar.checkbox('DEM', False):
    geojson_path = 'Reprojected_Rasterized_DEM.geojson'

    geojson_data = load_geojson(geojson_path)
    print(geojson_data)
    bitmap_layer = pdk.Layer(
    "GeoJsonLayer",
    data=geojson_data,
    opacity=0.01,
    stroked=True,
    filled=True,
    extruded=False,
    wireframe=False
)
else:
    bitmap_layer = None

if st.sidebar.checkbox('Landcover', True):
    # geojson_path_UK_LC_Grid_SoilErosion1 = 'UK_LC_Grid_SoilErosion1.geojson'

    # geojson_UK_LC_Grid_SoilErosion1 = load_geopackage(geojson_path_UK_LC_Grid_SoilErosion1)

    with open("UK_LC_Grid_SoilErosion1.geojson", "r") as geo_file:
        geojson_data = json.load(geo_file)

    geojson_UK_layer = pdk.Layer(
        "GeoJsonLayer",
        data = geojson_data,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        get_radius=1000,
    )
else:
    geojson_UK_layer = None




if st.sidebar.checkbox('Rainfall', True):
    stations_df = pd.read_csv('RainfallStations.csv')



    # Add rainfall data to stations DataFrame
    stations_df['Average_Rainfall'] = stations_df['Stations'].apply(lambda x: process_rainfall(f"Rainfall/{x}.csv"))
    

    rainfall_layer = pdk.Layer(
    'ScatterplotLayer',
    data=stations_df,
    get_position=['Longitude', 'Latitude'],
    get_color='[0, 0, 255, 160]',  
    get_radius='Average_Rainfall * 1000'  
)
else:
    rainfall_layer = None



# Display map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[erosion_layer, bitmap_layer, geojson_UK_layer, rainfall_layer]
))

