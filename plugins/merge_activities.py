from plugins.base_plugin import BasePlugin
from rich.console import Console

console = Console()

class MergeActivitiesPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "M"

    @property
    def description(self) -> str:
        return "Merge activities"

    def execute(self, api):
        console.print("Merging activities is not implemented yet.", style="bold red")
