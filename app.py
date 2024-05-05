import streamlit as st
import pandas as pd
import pydeck as pdk

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

df = load_data()

# Streamlit page setup
st.title('Soil Erosion Data Visualization')
st.sidebar.title('Layers')
# Legend display using markdown for colors
st.sidebar.header('Legend')
st.sidebar.markdown("""
- **No erosion detected**: ![ ](https://via.placeholder.com/15/000000/000000?text=+) 
- **0.01 - 1.00**: ![ ](https://via.placeholder.com/15/ffffb3/ffffb3?text=+) 
- **1.01 - 10.00**: ![ ](https://via.placeholder.com/15/8dd3c7/8dd3c7?text=+) 
- **10.01 - 100.00**: ![ ](https://via.placeholder.com/15/bebada/bebada?text=+) 
- **>100.00**: ![ ](https://via.placeholder.com/15/fb8072/fb8072?text=+) 
""")
# Map setup
view_state = pdk.ViewState(latitude=df['latitude'].mean(), longitude=df['longitude'].mean(), zoom=6)

# Adding layers based on checkboxes
if st.sidebar.checkbox('Show Erosion Sites', True):
    erosion_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position=['longitude', 'latitude'],
        get_color='color',
        get_radius='size',
        pickable=True
    )
else:
    erosion_layer = None

layers = [layer for layer in [erosion_layer] if layer is not None]

# Display map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=layers,
    tooltip={"text": "Erosion Rate: {Erosion_Rate}"}
))

