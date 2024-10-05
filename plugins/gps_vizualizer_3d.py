import pydeck as pdk
import requests
from plugins.base_plugin import BasePlugin
from plugins.plugin_types import PluginType
from rich.console import Console
from rich.panel import Panel
from enum import Enum
import os
import time
import shelve

console = Console()

class GPSVisualizer3dPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "V3D"

    @property
    def description(self) -> str:
        return "Visualize merged GPS data in 3D with elevation, fetching altitude if unavailable."

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_VISUALIZATION

    def __init__(self):
        self.cache_file = "elevation_cache.db"
        self.cache = shelve.open(self.cache_file)

    def __del__(self):
        self.cache.close()

    SUPPORTED_DATASETS = [
        'srtm90m',
        'srtm30m',
        'aster30m',
        # Add other supported datasets here
    ]

    def validate_locations(self, locations):
        """
        Validate that all locations have valid latitude and longitude values.

        Args:
            locations (list of tuples): List of (latitude, longitude) tuples.

        Returns:
            list: List of validated (latitude, longitude) tuples.
        """
        validated = []
        for idx, (lat, lon) in enumerate(locations):
            if not (-90 <= lat <= 90):
                console.print(f"Invalid latitude {lat} at index {idx}. Skipping this location.", style="yellow")
                continue
            if not (-180 <= lon <= 180):
                console.print(f"Invalid longitude {lon} at index {idx}. Skipping this location.", style="yellow")
                continue
            validated.append((lat, lon))
        return validated

    def fetch_elevations_opentopodata(self, locations, dataset='srtm90m'):
        """
        Fetch elevation data from OpenTopoData API.

        Args:
            locations (list of tuples): List of (latitude, longitude) tuples.
            dataset (str): Elevation dataset to use.

        Returns:
            list: Elevation values corresponding to the input locations.
        """
        elevations = []
        batch_size = 100  # OpenTopoData supports up to 100 locations per request
        endpoint = f"https://api.opentopodata.org/v1/{dataset}"

        for i in range(0, len(locations), batch_size):
            batch = locations[i:i + batch_size]
            locations_str = "|".join([f"{lat},{lon}" for lat, lon in batch])
            params = {"locations": locations_str}

            try:
                response = requests.get(endpoint, params=params, timeout=30)
                response.raise_for_status()
                results = response.json().get("results", [])

                if not results:
                    console.print(f"No results returned for batch {i // batch_size + 1}.", style="yellow")
                    elevations.extend([0] * len(batch))
                    continue

                for result in results:
                    elevation = result.get("elevation")
                    if elevation is not None:
                        elevations.append(elevation)
                    else:
                        console.print(f"No elevation data for ({result.get('location', {}).get('latitude')}, {result.get('location', {}).get('longitude')}). Using 0.", style="yellow")
                        elevations.append(0)

            except requests.HTTPError as http_err:
                console.print(f"HTTP error occurred: {http_err}", style="red")
                console.print(f"Response content: {response.text}", style="red")
                elevations.extend([0] * len(batch))
            except requests.RequestException as e:
                console.print(f"Request exception: {e}. Using 0 for these locations.", style="red")
                elevations.extend([0] * len(batch))

            # Respect rate limits by adding a short delay
            time.sleep(1)  # Adjust based on the API's rate limit policies

        return elevations

    def execute(self, data_dict, map_output_file="merged_map_3d.html", display=True, dataset='srtm90m'):
        # Validate dataset
        if dataset not in self.SUPPORTED_DATASETS:
            console.print(f"Unsupported dataset '{dataset}'. Please choose from {self.SUPPORTED_DATASETS}.", style="red")
            return

        data = data_dict.get("data", [])
        metadata = data_dict.get("metadata", {})

        if not data:
            console.print("No GPS data to visualize.", style="bold red")
            return

        # Extract coordinates
        raw_locations = [(point["lat"], point["lon"]) for point in data if "lat" in point and "lon" in point]
        validated_locations = self.validate_locations(raw_locations)

        if not validated_locations:
            console.print("No valid GPS locations to process after validation.", style="bold red")
            return

        # Fetch elevations
        console.print("Fetching elevation data from OpenTopoData...", style="bold cyan")
        elevations = self.fetch_elevations_opentopodata(validated_locations, dataset=dataset)  # Choose dataset as needed

        # Assign elevations back to data points
        elevation_idx = 0
        for point in data:
            if "lat" in point and "lon" in point:
                if (-90 <= point["lat"] <= 90) and (-180 <= point["lon"] <= 180):
                    point["alt"] = elevations[elevation_idx]
                    elevation_idx += 1
                else:
                    point["alt"] = 0  # Assign default elevation if coordinates are invalid
            else:
                point["alt"] = 0  # Assign default elevation if coordinates are missing

        # Debugging: Print elevations
        for idx, point in enumerate(data):
            console.print(f"Point {idx}: lat={point['lat']}, lon={point['lon']}, alt={point['alt']}", style="dim")

        # Extract coordinates and elevations
        coordinates = [(point["lon"], point["lat"], point["alt"]) for point in data]

        # Prepare data for pydeck
        path_data = {
            "path": [ [lon, lat, alt] for lon, lat, alt in coordinates ],
            "color": [ [0, 128, 200] for _ in coordinates ],  # Blue color for the path
        }

        # Determine elevation_scale dynamically
        max_elevation = max([point["alt"] for point in data])
        elevation_scale = 100 / max_elevation if max_elevation > 0 else 10

        # Define the initial view state with higher pitch for 3D effect
        initial_view_state = pdk.ViewState(
            longitude=coordinates[0][0],
            latitude=coordinates[0][1],
            zoom=14,
            pitch=45,  # Increased pitch for better 3D visualization
            bearing=0,
            height=600,
            width=800
        )

        # Define the path layer
        path_layer = pdk.Layer(
            "PathLayer",
            data=[path_data],
            get_path="path",
            get_width=5,
            get_color="color",
            width_min_pixels=2,
            elevation_scale=elevation_scale,  # Increased scale for visibility
            pickable=True,
            auto_highlight=True
        )

        # Define the scatter plot layer for start and end points
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=[
                {
                    "position": [coordinates[0][0], coordinates[0][1], coordinates[0][2]],
                    "color": [0, 255, 0],  # Green for start
                    "radius": 200  # Increased radius for better visibility
                },
                {
                    "position": [coordinates[-1][0], coordinates[-1][1], coordinates[-1][2]],
                    "color": [255, 0, 0],  # Red for end
                    "radius": 200
                }
            ],
            get_position="position",
            get_color="color",
            get_radius="radius",
            radius_min_pixels=5,
            pickable=True,
            auto_highlight=True
        )

        # Combine all layers
        layers = [
            path_layer,
            scatter_layer
        ]

        # Create the deck.gl map
        deck = pdk.Deck(
            layers=layers,
            initial_view_state=initial_view_state,
            tooltip={"text": "Elevation: {alt} meters"},
            map_style='mapbox://styles/mapbox/light-v9'  # Optional: Choose a map style
        )

        # Save the deck to an HTML file
        deck.to_html(map_output_file, notebook_display=False)

        if display:
            console.print(
                Panel(
                    f"3D animated map has been created and saved to {map_output_file}",
                    style="bold green"
                )
            )

        return map_output_file
