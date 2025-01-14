from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app_name")

LOCATION_COORDINATES = {
    "Matsuyama": (33.839, 132.765),        # Matsuyama Castle, Dogo Onsen
    "Takamatsu": (34.3428, 134.0466),      # Ritsurin Garden, Takamatsu Castle
    "Kochi": (33.5597, 133.5311),          # Kochi Castle, Katsurahama Beach
    "Tokushima": (34.0703, 134.5548),      # Awa Odori Festival, Mount Bizan
    "Naruto": (34.1765, 134.6081),         # Naruto Whirlpools, Otsuka Museum of Art
    "Kotohira": (34.1949, 133.8052),       # Kotohira-gu Shrine (Kompira-san)
    "Uwajima": (33.2231, 132.5603),        # Uwajima Castle, Taga Shrine
    "Iya Valley": (33.9333, 133.8333),     # Vine Bridges, Oboke Gorge
    "Shodoshima": (34.4799, 134.3050),     # Olive Park, Kankakei Gorge
    "Dogo Onsen": (33.8544, 132.7966),     # Historic hot spring bathhouse
    "Mount Ishizuchi": (33.7678, 133.1211),# Highest peak in Shikoku
    "Cape Ashizuri": (32.7264, 133.0250),  # Southernmost point of Shikoku
    "Oboke Gorge": (33.8800, 133.7833),    # Scenic river gorge
    "Ritsurin Garden": (34.3400, 134.0433),# Historic Japanese garden in Takamatsu
    "Muroto": (33.286, 134.15),            # Muroto Cape, Shinshō-ji Temple
}


def get_gps_coordinates(location_name: str) -> tuple:
    try:
        if location_name in LOCATION_COORDINATES:
            return LOCATION_COORDINATES[location_name]
        return fetch_coordinates_from_api(location_name)
    except Exception as e:
        print(f"Error fetching coordinates for {location_name}: {e}")
        return None


def fetch_coordinates_from_api(location_name: str) -> tuple:
    try:
        # Use the geolocator to get the location
        location = geolocator.geocode(location_name, exactly_one=True)
        if location is None:
            raise ValueError(f"Location not found: {location_name}")
        
        # Extract latitude and longitude
        return (location.latitude, location.longitude)
    except Exception as e:
        print(f"Error fetching coordinates for {location_name}: {e}")
        return None