import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_APIKEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather_by_coordinates(coordinates: tuple) -> dict:
    """
    Fetch current weather data from OpenWeatherMap API using latitude and longitude.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        dict: A dictionary containing weather details such as temperature, pressure,
              humidity, and description. Returns an error message if the location is not found.
    """
    
    try:
        # Construct the complete API URL
        complete_url = f"{BASE_URL}lat={coordinates[0]}&lon={coordinates[1]}&appid={API_KEY}"
        
        # Make the API request
        response = requests.get(complete_url)
        
        # Parse the response JSON
        weather_data = response.json()
        
        # Check if the response contains weather data
        if weather_data["cod"] != "404":
            main = weather_data.get("main", {})
            weather = weather_data.get("weather", [{}])[0]
            
            # Extract relevant details
            return {
                "temperature": main.get("temp"),
                "pressure": main.get("pressure"),
                "humidity": main.get("humidity"),
                "description": weather.get("description"),
            }
        else:
            return {"error": "Location not found"}
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}