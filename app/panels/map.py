from services.map import get_gps_coordinates
import folium
from streamlit_folium import st_folium
from services.weather import get_weather_by_coordinates


# Function to create weather data
def create_weather_data(data):
    weather_data = []
    weather_data_w_unit_info = []
    for _, row in data.iterrows():
        # Get GPS coordinates
        coordinates = get_gps_coordinates(row["location"])
        if not coordinates:
            continue

        # Fetch weather data using the coordinates
        weather_info = get_weather_by_coordinates(coordinates)
        weather_data.append({
            "location_name": row["location"],
            "coordinates": coordinates,
            "weather": weather_info,
        })
        
        weather_data_w_unit_info.append({
            "units": row["units"],
            "location": row["location"],
            "type": row["type"],
            "startup_cost": row["startup_cost"],
            "operating_cost": row["operating_cost"],
            "shutdown_cost": row["shutdown_cost"],
            "max_output": row["max_output"],
            "location_name": row["location"],
            "coordinates": coordinates,
            "weather": weather_info,
            
        })
    return weather_data, weather_data_w_unit_info


# Function to render the map
def render_map(weather_data):
    m = folium.Map(location=(33.75, 136.5), zoom_start=8)  # Central location

    for entry in weather_data:
        coordinates = entry["coordinates"]

        # Prepare popup content with unit and weather information
        popup_content = f"""
        <strong>{entry['units']}</strong><br>
        Location: {entry['location_name']}<br>
        Type: {entry['type']}<br>
        Startup Cost: {entry['startup_cost']}<br>
        Operating Cost: {entry['operating_cost']}<br>
        Shutdown Cost: {entry['shutdown_cost']}<br>
        Max Output: {entry['max_output']}<br><br>
        """

        # Add marker to the map
        folium.Marker(
            coordinates,
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=entry["units"],
        ).add_to(m)

    # Render the map
    st_folium(m, height=400, width=2200)