from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
from rich.console import Console
from plugins.plugin_types import PluginType
from enum import Enum

console = Console()

class GetLastActivityPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "7"

    @property
    def description(self) -> str:
        return "Get last activity"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api):
        last_activity = api.get_last_activity()
        if last_activity:
            viewer = DataViewer([last_activity])
            viewer.view_data()
        else:
            console.print("No last activity found.", style="bold yellow")
        return last_activity