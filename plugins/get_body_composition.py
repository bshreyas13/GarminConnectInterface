# plugins/get_body_composition.py

from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
import datetime
from plugins.plugin_types import PluginType
from enum import Enum

class GetBodyCompositionPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "5"

    @property
    def description(self) -> str:
        return "Get body composition data for today"
    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api, display=True):
        today = datetime.date.today()
        body_composition = api.get_body_composition(today.isoformat())
        if display:
            DataViewer.display_rich_output("Body Composition:", body_composition)
        return body_composition