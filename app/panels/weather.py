import streamlit as st
from graph.app.modules.data_models.external_source import WeatherData
from typing import List, Dict, Any


def parse_weather_data(data: List[Dict[str, Any]]) -> WeatherData:
    """
    Parses a list of weather data dictionaries into a WeatherData instance.

    Args:
        data (List[Dict[str, Any]]): The input weather data list.

    Returns:
        WeatherData: The parsed WeatherData instance.
    """
    weather_data = WeatherData()

    for entry in data:
        weather_data.location_name.append(entry["location_name"])
        weather_data.coordinates.append(entry["coordinates"])
        weather_data.weather_info.append(entry["weather"])

    return weather_data


def _get_weather_icon_code(description: str) -> str:
    """
    Get the appropriate weather icon code based on the weather description.
    
    Args:
        description (str): The description of the weather forecast.
        
    Returns:
        str: The icon code for the weather condition.
    """
    # Map common weather descriptions to OpenWeatherMap icon codes
    weather_icons = {
        "clear sky": "01d",
        "few clouds": "02d",
        "scattered clouds": "03d",
        "broken clouds": "04d",
        "shower rain": "09d",
        "rain": "10d",
        "thunderstorm": "11d",
        "snow": "13d",
        "mist": "50d",
        "overcast clouds": "04d",
    }
    
    # Return the corresponding icon code or a default value
    return weather_icons.get(description.lower(), "01d")

def render_weather_panels(weather_data, num_columns=2):
    """
    Render weather panels in a grid layout with icons on the left and data on the right.

    Args:
        weather_data (list of dict): List of weather data dictionaries.
        num_columns (int): Number of columns per row.
    """
    rows = [weather_data[i:i + num_columns] for i in range(0, len(weather_data), num_columns)]
    
    for row in rows:
        cols = st.columns(len(row))
        for col, location_weather in zip(cols, row):
            if "error" in location_weather["weather"]:
                col.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        padding: 10px;
                        text-align: center;
                        background: #f8d7da;
                        color: #721c24;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    ">
                        <strong>{location_weather["location_name"]}</strong>
                        <p>{location_weather["weather"]["error"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                weather = location_weather["weather"]
                icon_code = _get_weather_icon_code(weather["description"])
                temperature_celsius = round(weather["temperature"] - 273.15, 2)

                col.markdown(
                    f"""
                    <div style="
                        display: flex;
                        align-items: center;
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        padding: 10px;
                        background: White;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    ">
                        <div style="flex: 1; text-align: center;">
                            <img src="https://openweathermap.org/img/wn/{icon_code}@2x.png" alt="Weather Icon" style="width: 50px; height: 50px;">
                        </div>
                        <div style="flex: 3; padding-left: 10px;">
                            <h4 style="margin: 0;">{location_weather["location_name"]}</h4>
                            <p style="margin: 0;"><strong>Temp:</strong> {temperature_celsius} °C</p>
                            <p style="margin: 0;"><strong>Pressure:</strong> {weather["pressure"]} hPa</p>
                            <p style="margin: 0;"><strong>Humidity:</strong> {weather["humidity"]}%</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )