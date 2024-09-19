
from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
import datetime
from plugins.plugin_types import PluginType
from enum import Enum

class GetUserSummaryPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "4"

    @property
    def description(self) -> str:
        return "Get User Summary"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api, display=True):
        today = datetime.date.today()
        user_summary = api.get_user_summary(today.isoformat())
        if display:
            DataViewer.display_rich_output("User Summary:", user_summary)

        return user_summary