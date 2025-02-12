import streamlit as st

# Set up Streamlit page config
st.set_page_config(
    page_title="Streamlit Dublin Bus Times",
    page_icon="assets/images/dublin_bus_favicon.png",
    layout="centered",
)

import os
import folium
from streamlit_folium import st_folium
from modules.STutils import load_routes, load_directions, load_stops, get_upcoming_buses,convert_gtfs_time
from modules.Styles import apply_sidebar_styles, apply_dropdown_styles, apply_global_styles, apply_button_styles, apply_table_styles, display_centered_logo, suppress_insecure_request_warnings, apply_map_styles, hide_streamlit_spinner

# Suppress warnings globally
suppress_insecure_request_warnings()

# Apply styles
hide_streamlit_spinner()
apply_global_styles() 
apply_sidebar_styles()
apply_dropdown_styles()
apply_button_styles()
apply_map_styles()

# Header layout for consistent style
col1, col2 = st.columns([3, 3])
with col1:
    st.title("Bus Times")
with col2:
    st.image("assets/images/dublin_bus_logo.png", width=300)

st.write("Visualising real-time stop updates for Dublin buses using JSON formatted data.")

# Visualize empty map
def visualise_map():
    return folium.Map(location=[53.3498, -6.2603], zoom_start=12)


# Visualize stops on the map with pre-colored pin icons
def visualise_stops(stops_df):
    stop_map = folium.Map(location=[53.3498, -6.2603], zoom_start=12)

    # Paths to the pre-colored pin icons
    icon_paths = {
        "green": os.path.join("assets", "images", "pin_green.png"),
        "blue": os.path.join("assets", "images", "pin_blue.png"),
        "red": os.path.join("assets", "images", "pin_red.png"),
    }

    for _, stop in stops_df.iterrows():
        # Determine the color based on the stop type
        color = "green" if stop["trip_starts"] == 1 else "red" if stop["trip_ends"] == 1 else "blue"
        
        # Use the pre-colored pin icon
        icon = folium.CustomIcon(
            icon_image=icon_paths[color],
            icon_size=(40, 40)  # Adjust the size as needed
        )

        # Add a marker with the colored pin icon
        folium.Marker(
            location=[stop["stop_lat"], stop["stop_lon"]],
            popup=f"{stop['stop_full']}",
            tooltip=f"{stop['stop_name']}",
            icon=icon
        ).add_to(stop_map)

    return stop_map


# Load Routes
routes_df = load_routes()

# Dropdown for selecting route
selected_route_name = st.selectbox("Select a Route", ["Select a Route"] + routes_df["route_name"].tolist())

if selected_route_name != "Select a Route":
    selected_route_row = routes_df[routes_df["route_name"] == selected_route_name]
    selected_route_id = selected_route_row["route_id"].values[0]

    # Load Directions
    directions_df = load_directions(selected_route_id)
    direction_options = ["Select Direction"] + directions_df["trip_headsign"].tolist()
    selected_direction = st.selectbox("Select Direction", direction_options)

    if selected_direction != "Select Direction":
        trip_id = directions_df[directions_df["trip_headsign"] == selected_direction]["trip_id"].values[0]
        direction_id = directions_df[directions_df["trip_headsign"] == selected_direction]["direction_id"].values[0]

        # Load Stops
        stops_df = load_stops(trip_id)

        if not stops_df.empty:
            # Display stops on the map
            stop_map = visualise_stops(stops_df)
            st_folium(stop_map, width=1000, height=700)

            # Dropdown for selecting a stop
            selected_stop = st.selectbox("Select Stop", ["Select a Stop"] + stops_df["stop_full"].tolist())

            if selected_stop != "Select a Stop":
                stop_id = stops_df[stops_df["stop_full"] == selected_stop]["stop_id"].values[0]

                if st.button("🚌 Show Upcoming Buses"):
                    # Create a placeholder for the "Running..." widget
                    running_placeholder = st.empty()
    
                    # Display the running message
                    running_placeholder.markdown("### 🕒 Calculating Times...")
                    
                    # Fetch upcoming buses
                    upcoming_buses_df = get_upcoming_buses(selected_route_id, direction_id, stop_id)
                    
                    # Clear the "Running..." message
                    running_placeholder.empty()

                    if upcoming_buses_df.empty:
                        st.warning(
                            f"""
                            No upcoming buses for the selected stop: **{selected_stop}**.  
                            Please check the [Dublin Bus Timetables](https://www.dublinbus.ie/timetables).  

                            If all routes show no updates, please download folder **GTFS_Dublin_Bus.zip**  
                            from the transport operator [Dublin Bus](https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip).  

                            After unzipping, check the `routes.txt` file and ensure the `route_id` matches  
                            the one shown in the API endpoint.
                            """
                        )
                    else:
                        st.success(f"🕒 Upcoming buses for stop **{selected_stop}**:")

                        # Sort and display the data
                        df = upcoming_buses_df.sort_values(by="minutes_left").rename(columns={
                            'trip_id': 'Trip',
                            'minutes_left': 'Minutes'
                        }).reset_index(drop=True)

                        # Display the styled DataFrame
                        st.markdown(apply_table_styles(df), unsafe_allow_html=True)

        else:
            # Show an empty map if there are no stops
            st_folium(visualise_map(), width=1000, height=700)

    else:
        # Show an empty map if no direction is selected
        st_folium(visualise_map(), width=1000, height=700)

else:
    # Show an empty map if no route is selected
    st_folium(visualise_map(), width=1000, height=700)

# Add TFI Logo at the Bottom
st.markdown("<br><hr>", unsafe_allow_html=True)
display_centered_logo("assets/images/tfi_logo.png", width=300)
