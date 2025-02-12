import io
import re
import zipfile
import requests
import pandas as pd
import streamlit as st

### 12-02-2025 Final fix for the NTA static data 😎 🚀 

# Define GTFS URL
GTFS_URL = "https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip"

# Step 1: Download GTFS ZIP file into memory
@st.cache_data
def fetch_gtfs_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return zipfile.ZipFile(io.BytesIO(response.content), "r")
    else:
        raise RuntimeError("Failed to download GTFS data.")

# Step 2: Read a file from the ZIP directly into a DataFrame
@st.cache_data
def read_txt_from_zip(zip_file, filename):
    with zip_file.open(filename) as file:
        return pd.read_csv(file)

# Step 3: Process routes.txt
@st.cache_data
def process_routes(routes_df):
    """Processes routes.txt and adds a concatenated route name."""
    cleaned_routes = routes_df[["route_id", "route_short_name", "route_long_name"]].copy()
    cleaned_routes["route_concat"] = cleaned_routes["route_short_name"].astype(str) + ". " + cleaned_routes["route_long_name"]

    def custom_sort_key(route_short_name):
        match = re.match(r'(\d+)([A-Za-z]*)', route_short_name)
        if match:
            num_part = int(match.group(1))
            alpha_part = match.group(2)
            return (num_part, alpha_part or "")
        return (float('inf'), route_short_name)

    cleaned_routes["sort_key"] = cleaned_routes["route_short_name"].apply(custom_sort_key)
    cleaned_routes = cleaned_routes.sort_values(by="sort_key").drop(columns=["sort_key"])
    cleaned_routes = cleaned_routes.reset_index(drop=True)

    cleaned_routes = cleaned_routes[["route_id", "route_short_name", "route_concat"]].copy()
    cleaned_routes.rename(columns={"route_short_name": "incoming_bus", "route_concat": "route_name"}, inplace=True)

    return cleaned_routes

# Step 4: Process trips.txt
@st.cache_data
def process_trips(trips_df):
    """Process trips.txt to create Towards.txt with unique route_id, trip_headsign, and direction_id."""
    return trips_df[['route_id', 'trip_id', 'trip_headsign', 'direction_id']] \
        .drop_duplicates(subset=['route_id', 'trip_headsign', 'direction_id'], keep='first') \
        .sort_values(by='route_id')

# Step 5: Process stop_times.txt
@st.cache_data
def process_stop_times(stop_times_df, trips_df, routes_df):
    """Processes stop_times.txt and merges with trips and routes to create StopTimesPerTrip.txt."""
    
    trips_df = trips_df.merge(routes_df[["route_id", "route_name", "incoming_bus"]], on="route_id", how="left")
    trips_df = trips_df[["trip_id", "route_id", "incoming_bus", "route_name", "trip_headsign", "direction_id"]].copy()
    return stop_times_df[["trip_id", "stop_id", "arrival_time"]].copy()

# Step 6: Process StopMapLocation.txt
@st.cache_data
def process_stop_map_location(stop_times_df, stops_df, SelectDirection_df):
    """Processes stops.txt and stop_times.txt to generate StopMapLocation.txt."""
    
    SelectDirection_df["rout_dir_id_concat"] = SelectDirection_df["route_id"] + SelectDirection_df["direction_id"].astype(str)
    SelectDirection_df1 = SelectDirection_df[["trip_id", "route_id", "direction_id", "rout_dir_id_concat"]].copy()

    stops_df["stop_full"] = stops_df["stop_code"].astype(str) + " - " + stops_df["stop_name"]
    filtered_stop_times_df = stop_times_df[stop_times_df["trip_id"].isin(SelectDirection_df1["trip_id"])]
    StopByTrip_df = filtered_stop_times_df[["trip_id", "stop_id", "stop_sequence", "stop_headsign", "pickup_type", "drop_off_type"]].copy()

    StopByTrip_df.rename(columns={"pickup_type": "trip_ends", "drop_off_type": "trip_starts"}, inplace=True)
    StopByTrip_df = StopByTrip_df.merge(stops_df, on="stop_id", how="left")
    StopByTrip_df = StopByTrip_df.merge(SelectDirection_df1, on="trip_id", how="left")
    StopByTrip_df.rename(columns={"rout_dir_id_concat": "concat"}, inplace=True)

    return StopByTrip_df[[
        "route_id", "trip_id", "direction_id", "concat", "stop_id", "stop_code",
        "stop_name", "stop_full", "stop_headsign", "stop_sequence", "stop_lat",
        "stop_lon", "trip_starts", "trip_ends"
    ]].copy()

# Load GTFS Data when the module is imported
try:
    print("Downloading GTFS data...")
    gtfs_zip = fetch_gtfs_data(GTFS_URL)
    print("Download complete!")

    print("Extracting required files from ZIP...")
    routes_df = read_txt_from_zip(gtfs_zip, "routes.txt")
    trips_df = read_txt_from_zip(gtfs_zip, "trips.txt")
    stop_times_df = read_txt_from_zip(gtfs_zip, "stop_times.txt")
    stops_df = read_txt_from_zip(gtfs_zip, "stops.txt")

    print("Processing routes.txt...")
    Routes = process_routes(routes_df)
    print("Processing trips.txt...")
    Towards = process_trips(trips_df)
    print("Processing stop_times.txt and merging with trips/routes...")
    StopTimesPerTrip = process_stop_times(stop_times_df, trips_df, Routes)
    print("Processing StopMapLocation.txt...")
    StopMapLocation = process_stop_map_location(stop_times_df, stops_df, Towards)

    print("Data preparation complete!")

except Exception as e:
    print(f"Error during data preparation: {e}")
    Routes, Towards, StopTimesPerTrip, StopMapLocation = None, None, None, None
