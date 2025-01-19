import requests
import pandas as pd
import streamlit as st

# Securely load the API from key st.secrets
YOUR_API_KEY = st.secrets["API_KEY"]

# API details
API_URL = "https://api.nationaltransport.ie/gtfsr/v2/Vehicles?format=json"

# Load Routes.txt
@st.cache_data
def load_routes():
    return pd.read_csv("assets/data/Routes.txt")

# Load Towards.txt
@st.cache_data
def load_directions():
    return pd.read_csv("assets/data/Towards.txt")

# Fetch Vehicles Data
@st.cache_data(ttl=60)
def fetch_vehicles_data():
    headers = {"x-api-key": YOUR_API_KEY}
    try:
        response = requests.get(API_URL, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Filter Vehicles Data by 'concat' (route_id + direction_id)
def fetch_buses_by_route_direction(concat):
    data = fetch_vehicles_data()
    
    if data is None:
        return pd.DataFrame()
    
    buses = []
    
    for entity in data.get("entity", []):
        trip_info = entity.get("vehicle", {}).get("trip", {})
        position_info = entity.get("vehicle", {}).get("position", {})

        route_id = trip_info.get("route_id")
        direction_id = trip_info.get("direction_id")
        combined_id = str(route_id) + str(direction_id)

        if combined_id == concat:
            buses.append({
                "trip_id": trip_info.get("trip_id"),
                "route_id": route_id,
                "direction_id": direction_id,
                "vehicle_id": entity.get("vehicle", {}).get("vehicle", {}).get("id"),
                "start_time": trip_info.get("start_time"),
                "start_date": trip_info.get("start_date"),
                "latitude": position_info.get("latitude"),
                "longitude": position_info.get("longitude"),
            })

    return pd.DataFrame(buses)

