import os
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from modules.BLutils import load_routes, load_directions, fetch_buses_by_route_direction
from modules.Styles import apply_sidebar_styles, apply_dropdown_styles, apply_global_styles, apply_button_styles, apply_table_styles,display_centered_logo, suppress_insecure_request_warnings, apply_map_styles,hide_streamlit_spinner

# Suppress warnings globally
suppress_insecure_request_warnings()

# Set up Streamlit page config
st.set_page_config(
    page_title="Streamlit Dublin Bus Locator",
    page_icon="assets/images/dublin_bus_favicon.png",
    layout="centered",
)

# Visualize map without buses
def visualise_map():
    return folium.Map(location=[53.3498, -6.2603], zoom_start=12)


    # Visualize buses on the map with custom bus icons
def visualise_buses(data):
    bus_map = folium.Map(location=[53.3498, -6.2603], zoom_start=12)

    # Path to the custom bus icon
    bus_icon_url = os.path.join("assets", "images", "bus.png")

    for _, row in data.iterrows():
        lat, lon = row["latitude"], row["longitude"]

        if pd.notnull(lat) and pd.notnull(lon):
            # Use the custom bus icon
            icon = folium.CustomIcon(
                icon_image=bus_icon_url,  # Path to the custom icon
                icon_size=(40, 40)  # Adjust size as needed
            )

            # Add a marker to the map
            folium.Marker(
                location=[lat, lon],
                popup=f"<b>Trip ID:</b> {row['trip_id']}<br>"
                      f"<b>StartTime:</b> {row['start_time']}<br>"
                      f"<b>Vehicle ID:</b> {row['vehicle_id']}<br>",
                icon=icon
            ).add_to(bus_map)

    return bus_map

# Main Streamlit app
def main():
    hide_streamlit_spinner()
    apply_sidebar_styles()
    apply_dropdown_styles()
    apply_global_styles()
    apply_button_styles()
    apply_map_styles()

    col1, col2 = st.columns([3, 3])
    with col1:
        st.title("Bus Locator")
    with col2:
        st.image("assets/images/dublin_bus_logo.png", width=300)

    st.write("Visualising real-time locations of Dublin buses using GTFS JSON formatted data.")

    # Load route and direction data
    routes_df, directions_df = load_routes(), load_directions()

    # Dropdown for selecting route
    selected_route_name = st.selectbox("Select a Route", ["Dublin Bus Routes"] + routes_df["route_name"].tolist())

    if selected_route_name != "Dublin Bus Routes":
        selected_route_row = routes_df[routes_df["route_name"] == selected_route_name]
        selected_route_id = selected_route_row["route_id"].values[0]

        # Filter directions based on selected route and add default "Select Direction"
        direction_options = ["Select Direction"] + directions_df[directions_df["route_id"] == selected_route_id]["trip_headsign"].tolist()
        selected_direction = st.selectbox("Select Direction", direction_options)

        # Proceed only if a valid direction is selected
        if selected_direction != "Select Direction":
            # Get direction_id based on selection
            selected_direction_id = directions_df[
                (directions_df["route_id"] == selected_route_id) & 
                (directions_df["trip_headsign"] == selected_direction)
            ]["direction_id"].values[0]

            # Create 'concat' for filtering
            concat = str(selected_route_id) + str(selected_direction_id)

            # Fetch and display bus data AFTER both selections
            bus_data = fetch_buses_by_route_direction(concat)

            if bus_data.empty:
                st.warning(
                f"""
                No buses are currently operating for the selected route: **{selected_route_name}**.  
                Please check the [Dublin Bus Timetables](https://www.dublinbus.ie/timetables).  

                If all routes show no updates, please download folder **GTFS_Dublin_Bus.zip**  
                from the transport operator [Dublin Bus](https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip).  

                After unzipping, check the `routes.txt` file and ensure the `route_id` matches  
                the one shown in the API endpoint.
                """
            )
            else:

                # Map Visualization
                bus_map = visualise_buses(bus_data)
                st_folium(bus_map, width=1000, height=700)

                if st.button("🔄 Refresh Bus Data"):
                    # Clear session state
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]

                    # Force app refresh by setting a placeholder value in session state
                    st.session_state["_app_refresh"] = True

                # Display trip_id and start_time sorted by start_time
                st.success(f"🚌 Buses operating route **{selected_route_name}** towards **{selected_direction}**:")

                # Sort by start_time and rename columns
                bus_data_sorted = bus_data.sort_values(by="start_time", ascending=True).reset_index(drop=True)
                df = pd.DataFrame(bus_data_sorted)[["trip_id", "start_time"]].rename(columns={
                    "trip_id": "Trip",
                    "start_time": "StartTime"
                })

                # Display the styled DataFrame as HTML
                st.markdown(apply_table_styles(df), unsafe_allow_html=True)

        else:
            # Show an empty map if no direction is selected
            st_folium(visualise_map(), width=1000, height=700)
    else:
        # Show an empty map if no route is selected
        st_folium(visualise_map(), width=1000, height=700)

    # Add TFI logo at the bottom
    st.markdown("<br><hr>", unsafe_allow_html=True)
    display_centered_logo("assets/images/tfi_logo.png", width=300)

if __name__ == "__main__":
    main()