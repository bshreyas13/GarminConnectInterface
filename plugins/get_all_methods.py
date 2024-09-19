from plugins.base_plugin import BasePlugin
from rich.console import Console
from rich.table import Table
from rich.text import Text
from plugins.plugin_types import PluginType
from enum import Enum

console = Console()

class GetAllMethodsPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "H"

    @property
    def description(self) -> str:
        return "(Dev options) Display all available methods in Garmin API with docstrings"
    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api, display=True):
        table = Table(title="Garmin Connect API Methods", show_header=True, header_style="bold magenta")
        table.add_column("Method", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")

        methods = [method for method in dir(api) if callable(getattr(api, method)) and not method.startswith("_")]
        
        for method in sorted(methods):
            doc = getattr(api, method).__doc__
            if doc:
                summary, *details = doc.strip().split('\n', 1)
                summary = summary.strip()
                details = '\n'.join(details).strip() if details else ""

                description = Text(summary)
                if details:
                    description.append("\n\n" + details, style="dim")

                table.add_row(method, description)

        console.print(table)
        console.print("\nPress any key to continue...", style="bold yellow")
        input()
        return None