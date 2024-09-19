from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
from plugins.plugin_types import PluginType
from enum import Enum

class GetActiveGoalsPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "9"

    @property
    def description(self) -> str:
        return "Get active goals"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api, display=True):
        active_goals = api.get_goals("active")
        if display:
            DataViewer.display_rich_output("Active Goals:", active_goals)

        return active_goals