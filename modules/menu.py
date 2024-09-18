from typing import Dict
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class Menu:
    """
    The Menu class provides a simple interface for creating and displaying a menu with selectable options.
    Attributes:
        options (Dict[str, str]): A dictionary to store menu options with their keys and descriptions.
    Methods:
        __init__():
            Initializes the Menu instance with an empty options dictionary.
        add_option(key: str, description: str) -> None:
            Adds an option to the menu with the given key and description.
        display() -> None:
            Displays the menu options in a formatted table using the rich library.
        get_selection() -> str:
            Prompts the user to make a selection from the available menu options and returns the selected key.
    """
    def __init__(self):
        self.options: Dict[str, str] = {}

    def add_option(self, key: str, description: str) -> None:
        """
        Adds an option to the menu.

        Args:
            key (str): The key for the option.
            description (str): The description of the option.

        Returns:
            None
        """
        self.options[key] = description

    def display(self) -> None:
        """
        Displays a menu using the rich library's Table component.
        This method creates a table with two columns: "Key" and "Description".
        It iterates over the `self.options` dictionary, adding each key and its
        corresponding description as a row in the table. Finally, it prints the
        table to the console.
        Returns:
            None
        """
        table = Table(title="Garmin Connect API Menu")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")

        for key, description in self.options.items():
            table.add_row(key, description)

        console.print(table)

    def get_selection(self) -> str:
        """
        Prompts the user to make a selection from the available options.

        Returns:
            str: The user's selection as a string.
        """
        return Prompt.ask("Make your selection", choices=list(self.options.keys()))
