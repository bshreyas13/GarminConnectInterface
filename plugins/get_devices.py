from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer

class GetDevicesPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "0"

    @property
    def description(self) -> str:
        return "Get Garmin devices"

    def execute(self, api):
        devices = api.get_devices()
        DataViewer.display_rich_output("Devices:", devices)
        return devices