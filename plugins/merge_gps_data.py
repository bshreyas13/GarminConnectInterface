from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
from plugins.plugin_types import PluginType
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from datetime import datetime
from enum import Enum

console = Console()

class MergeGPSDataPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "G"

    @property
    def description(self) -> str:
        return "Merge GPS data from multiple activities.(Requires Processed or retrived activites)"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.SECONDARY_PROCESSING

    def execute(self, api, activities, display=True):
        # Extract activity IDs and start times
        activity_info = []
        for a in activities:
            activity_id = a.get("activityId")
            # Fetch the activity summary to get the start time
            start_time_str = a.get("startTimeLocal")
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            activity_info.append({"activityId": activity_id, "startTime": start_time, "startTimeLocal": start_time_str})

        # Sort activities by start time
        activity_info.sort(key=lambda x: x["startTime"])

        if display:
            DataViewer.display_rich_output(
                f"Found {len(activity_info)} activities sorted by start time:",
                [(a["activityId"], a["startTimeLocal"]) for a in activity_info],
            )

        # Initialize list to hold merged GPS data
        merged_gps_data = {}
        merged_gps_data["metadata"] = {"activity_ids": [info["activityId"] for info in activity_info],
                                          "start_times": [info["startTime"] for info in activity_info],
                                          "stop_indicies" : [0],
                                          "drop_stop_indicies" : []

                                        }
        merged_gps_data["data"] = []

        for info in activity_info:
            activity_id = info["activityId"]
            activity_details = api.get_activity_details(activity_id)
            gps_data = activity_details.get("geoPolylineDTO", {}).get("polyline", [])
            if gps_data:
                merged_gps_data["data"].extend(gps_data)
                merged_gps_data["metadata"]["stop_indicies"].append(len(merged_gps_data["data"]))
            else:
                console.print(f"No GPS data found for activity ID {activity_id}", style="bold yellow")
        
        drop_stops = Prompt.ask("Enter the stop indicies to drop (comma separated, assume 0 indexed list)", default=None)
        drop_stops = [int(i) for i in drop_stops.split(",")] if drop_stops else None

        if drop_stops:    
            merged_gps_data["metadata"]["drop_stop_indicies"] = drop_stops
            merged_gps_data["metadata"]["stop_indicies"] = [item for i, item in enumerate(merged_gps_data["metadata"]["stop_indicies"]) if i not in drop_stops]

        if not merged_gps_data:
            console.print("No GPS data available to merge.", style="bold red")
            return None

        if display:
            console.print(
                Panel.fit(
                    f"Merged GPS data from {len(activity_info)} activities.",
                    border_style='green',
                    style="bold green"
                )
            )

        return merged_gps_data
