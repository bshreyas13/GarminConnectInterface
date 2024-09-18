# plugins/get_unit_system.py

from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer

class GetUnitSystemPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "2"

    @property
    def description(self) -> str:
        return "Get unit system"

    def execute(self, api):
        unit_system = api.get_unit_system()
        DataViewer.display_rich_output("Unit System:", unit_system)
        return unit_system