from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
import datetime

class GetStatsPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "3"

    @property
    def description(self) -> str:
        return "Get activity data for today"

    def execute(self, api):
        today = datetime.date.today()
        stats = api.get_stats(today.isoformat())
        DataViewer.display_rich_output("Stats:", stats)
        return stats
    
