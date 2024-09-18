from plugins.base_plugin import BasePlugin
from rich.console import Console
from modules.data_viewer import DataViewer

class GetFullNamePlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "1"

    @property
    def description(self) -> str:
        return "Get full name"

    def execute(self, api):
        full_name = api.get_full_name()
        DataViewer.display_rich_output("Full Name:", full_name)
        return full_name
    



