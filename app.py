import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.features import DivIcon

# Load data from an Excel file
@st.cache_data
def load_data():
    sheet_id = "1SfiCfoi8H8niQ1UAh4uqI-aM2OiGnGKwogHVTqiIuFI"
    sheet_name = "Sheet1"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    
    # Read CSV
    df = pd.read_csv(csv_url)

    # Convert latitude & longitude to float
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    # Drop NaN values
    df = df.dropna(subset=["latitude", "longitude"])

    return df

df = load_data()

# Sidebar - Place selection
st.sidebar.title("📍 Click a Place")
show_labels = st.sidebar.checkbox("Show Labels", value=True)
if "selected_place" not in st.session_state:
    st.session_state["selected_place"] = "🏡 My Airbnb"

if st.sidebar.button("🏡 My Airbnb"):
    st.session_state["selected_place"] = "🏡 My Airbnb"

for _, row in df.iterrows():
    if st.sidebar.button(row["name"]):
        st.session_state["selected_place"] = row["name"]

# Toggle for showing labels

# Determine map center based on selected place
if st.session_state["selected_place"] == "🏡 My Airbnb":
    map_center = [13.722233,100.525416]  # Airbnb Location
else:
    selected_row = df[df["name"] == st.session_state["selected_place"]].iloc[0]
    map_center = [selected_row["latitude"], selected_row["longitude"]]

# Create map
m = folium.Map(location=map_center, zoom_start=14)

# Airbnb marker
folium.Marker(
    location=[13.7504, 100.5406],
    popup="🏡 My Airbnb",
    tooltip="My Airbnb",
    icon=folium.Icon(color="blue", icon="home"),
).add_to(m)

# Add all tourist locations
for _, row in df.iterrows():
    popup_content = f'''
    <div style="width: 300px;">
        <b style="font-size: 16px;">{row["name"]}</b><br>
        <img src="{row["image_url"]}" width="100%" style="border-radius: 10px;"><br>
        {row["description"]}<br>
        <a href="{row["google_maps_link"]}" target="_blank">📍 Open in Google Maps</a>
    </div>
    '''
    
    # Add marker with a label
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=folium.Popup(popup_content, max_width=320),
        tooltip=row["name"],
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

    # ✅ Only show labels if toggle is ON
    if show_labels:
        folium.map.Marker(
            location=[row["latitude"], row["longitude"]],
            icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12px; color: black; background-color: white; padding: 2px 5px; border-radius: 5px;">{row["name"]}</div>',
            ),
        ).add_to(m)

# Display map
st.title("🗺️ Bangkok Tourist Map")
st.write("Click on any location to open it in Google Maps or select a place from the sidebar.")
folium_static(m)
