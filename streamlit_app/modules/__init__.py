from .DataPrep import fetch_gtfs_data, read_txt_from_zip, process_routes, process_trips, process_stop_times, process_stop_map_location
import pandas as pd

# GTFS URL
GTFS_URL = "https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip"

def update_data():
    """Fetches GTFS data and processes required tables."""
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
        return Routes, Towards, StopTimesPerTrip, StopMapLocation

    except Exception as e:
        print(f"Error during data preparation: {e}")
        return None, None, None, None
