from typing import Dict
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class Menu:
    def __init__(self):
        self.options: Dict[str, str] = {}

    def add_option(self, key: str, description: str) -> None:
        self.options[key] = description

    def display(self) -> None:
        table = Table(title="Garmin Connect API Menu")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")

        for key, description in self.options.items():
            table.add_row(key, description)

        console.print(table)

    def get_selection(self) -> str:
        return Prompt.ask("Make your selection", choices=list(self.options.keys()))
