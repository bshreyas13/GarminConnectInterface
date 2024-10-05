import folium
from folium.plugins import TimestampedGeoJson
from plugins.base_plugin import BasePlugin
from plugins.plugin_types import PluginType
from rich.console import Console
from rich.panel import Panel
from datetime import datetime
from enum import Enum
console = Console()

class GPSVisualizer2dPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "v"

    @property
    def description(self) -> str:
        return "Visualize merged GPS data on a map with moving arrow"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_VISUALIZATION

    def execute(self, data_dict, map_output_file="merged_map.html", display=True):
        data = data_dict.get("data", [])
        metadata = data_dict.get("metadata", {})

        # Check if there's GPS data to visualize
        if not data or len(data) == 0:
            console.print("No GPS data to visualize.", style="bold red")
            return

        # Extract the starting point for initializing the map
        starting_point = data[0]
        lat = starting_point.get("lat")
        lon = starting_point.get("lon")

        # Initialize the map centered at the starting point
        map_object = folium.Map(location=[lat, lon], zoom_start=13)
        # Add OpenStreetMap tiles
        folium.TileLayer('OpenStreetMap').add_to(map_object)

        # Add Esri World Imagery (Satellite)
        folium.TileLayer('Esri.WorldImagery').add_to(map_object)

         # Add Google Satellite tiles
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',  # Satellite tiles
            attr='Google',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(map_object)

        # Add Google Maps (road map) tiles
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',  # Map tiles
            attr='Google Maps',
            name='Google Maps',
            overlay=False,
            control=True
        ).add_to(map_object)

        # Add Google Hybrid tiles (Satellite + Labels)
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',  # Hybrid (Satellite + Labels)
            attr='Google',
            name='Google Hybrid (Satellite + Labels)',
            overlay=False,
            control=True
        ).add_to(map_object)
        
        # Add LayerControl so the user can toggle between the tile layers
        folium.LayerControl().add_to(map_object)
        
        # Create PolyLine to connect the points into a line
        polyline = [(point["lat"], point["lon"]) for point in data]
        folium.PolyLine(locations=polyline, color="blue", weight=2.5).add_to(map_object)
        
        # Add markers for start and end points
        folium.Marker(location=[polyline[0][0], polyline[0][1]], popup="Start", icon=folium.Icon(color='green')).add_to(map_object)
        folium.Marker(location=[polyline[-1][0], polyline[-1][1]], popup="End", icon=folium.Icon(color='red')).add_to(map_object)

        #Add campsite markers
        for idx, stop_idx in enumerate(metadata.get("stop_indicies", [])):
            if idx == 0 or idx == len(metadata.get("stop_indicies", [])) - 1:
                continue
            stop_point = data[stop_idx]
           
            folium.Marker(location=[stop_point["lat"], stop_point["lon"]], popup=f"Campsite {idx}", icon=folium.Icon(color='orange')).add_to(map_object)

        # Prepare data for TimestampedGeoJson
        features = []
        for point in data:
            timestamp = datetime.utcfromtimestamp(point["time"] / 1000).isoformat()
            lat = point["lat"]
            lon = point["lon"]

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat],  # Note: GeoJSON uses [longitude, latitude]
                },
                "properties": {
                    "time": timestamp,
                    "style": {"color": "red"},
                    "icon": "circle",
                    "iconstyle": {
                        "fillColor": "blue",
                        "fillOpacity": 0.8,
                        "stroke": "true",
                        "radius": 2,
                    },
                },
            }
            features.append(feature)

        # Create the TimestampedGeoJson
        timestamped_geojson = TimestampedGeoJson(
            {
                "type": "FeatureCollection",
                "features": features,
            },
            period="PT1S",  # Time interval between frames
            add_last_point=True,
            auto_play=True,
            loop=False,
            max_speed=600000,
            loop_button=True,
            date_options="YYYY/MM/DD HH:mm:ss",
            time_slider_drag_update=True,
        )

        # Add the TimestampedGeoJson to the map
        timestamped_geojson.add_to(map_object)

        # Save the map to an HTML file
        map_object.save(map_output_file)

        if display:
            console.print(
                Panel(
                    f"Animated map has been created and saved to {map_output_file}",
                    style="bold green"
                )
            )

        return map_output_file
