import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load GTA and Toronto Hydro service area GeoJSON files
gta_geojson = '/Users/harshbhate/Codes/GTA-EV-Infrastructure/data/toronto_crs84.geojson'
ev_charing_station_geojson = '/Users/harshbhate/Codes/GTA-EV-Infrastructure/data/Toronto_City_EV_Chargers_WGS84.geojson'

gta = gpd.read_file(gta_geojson)
ev_stations = gpd.read_file(ev_charing_station_geojson)

# Initialize a Folium map centered on the GTA
m = folium.Map(location=[43.7, -79.4], zoom_start=10)

# Add the GTA boundaries
folium.GeoJson(gta, name='GTA').add_to(m)

# Filter Level 2 and Level 3 stations
level_2_stations = ev_stations[ev_stations['Level2_Charging_Ports'] > 0]
level_3_stations = ev_stations[ev_stations['Level3_Charging_Ports'] > 0]

# Sidebar or main area checkboxes for toggling layers
show_level_2 = st.checkbox('Show Level 2 Chargers', value=True)
show_level_3 = st.checkbox('Show Level 3 Chargers', value=True)

# Conditionally add Level 2 chargers to the map
if show_level_2:
    for _, station in level_2_stations.iterrows():
        centroid = station.geometry.centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=station['Location'],  # Replace with the appropriate field name
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

# Conditionally add Level 3 chargers to the map
if show_level_3:
    for _, station in level_3_stations.iterrows():
        centroid = station.geometry.centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=station['Location'],  # Replace with the appropriate field name
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

# Display the map in Streamlit
st.title("City-Operated EV Charging Stations in Greater Toronto Area")
st.write("This map displays the locations of city-operated electric vehicle charging stations in the Greater Toronto Area with options to view Level 2 or Level 3 chargers.")
st_folium(m, width=800, height=600)