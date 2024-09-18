from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
from rich.console import Console
from plugins.plugin_types import PluginType
from enum import Enum

console = Console()

class GetLastTenActivitiesPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "6"

    @property
    def description(self) -> str:
        return "Get last 10 activities"
    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api):
        last_ten_activities = api.get_activities(0, 10)
        if last_ten_activities:
            viewer = DataViewer(last_ten_activities)
            viewer.view_data()
        else:
            console.print("No activities found.", style="bold yellow")
        return last_ten_activities