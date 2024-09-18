from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
from plugins.plugin_types import PluginType
from enum import Enum

class GetDevicesPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "0"

    @property
    def description(self) -> str:
        return "Get Garmin devices"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api):
        devices = api.get_devices()
        DataViewer.display_rich_output("Devices:", devices)
        return devices