from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
import datetime
from plugins.plugin_types import PluginType
from enum import Enum  

class GetStatsPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "3"

    @property
    def description(self) -> str:
        return "Get activity data for today"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api, display=True):
        today = datetime.date.today()
        stats = api.get_stats(today.isoformat())
        if display:
            DataViewer.display_rich_output("Stats:", stats)
        return stats
    
