from plugins.base_plugin import BasePlugin
from rich.console import Console
from modules.data_viewer import DataViewer
from plugins.plugin_types import PluginType
from enum import Enum

class GetFullNamePlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "1"

    @property
    def description(self) -> str:
        return "Get full name"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api, display=True):
        full_name = api.get_full_name()
        if display:
            DataViewer.display_rich_output("Full Name:", full_name)
        return full_name
    



