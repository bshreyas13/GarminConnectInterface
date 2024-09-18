from plugins.base_plugin import BasePlugin
from rich.console import Console
from modules.data_viewer import DataViewer
from plugins.plugin_types import PluginType
from enum import Enum

console = Console()


class MergeActivitiesPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "M"

    @property
    def description(self) -> str:
        return "Merge activities. (Type of activities need to be same in the current implementation)"
    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_PROCESSING
    
    def execute(self, activities):
        # DataViewer.display_rich_output("Merging Activities", activities)
        console.print("Merging activities is not implemented yet.", style="bold red")
