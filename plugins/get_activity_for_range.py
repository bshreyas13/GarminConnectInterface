from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
from rich.console import Console
from rich.prompt import Prompt
from datetime import datetime

console = Console()

def get_valid_date(prompt_text: str) -> str:
    while True:
        date_str = Prompt.ask(prompt_text)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            console.print("Invalid date format. Please enter the date in YYYY-MM-DD format.", style="bold red")

class GetActivityForRangePlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "R"

    @property
    def description(self) -> str:
        return "Get activity data for a date range"

    def execute(self, api):
        def get_valid_date(prompt_text: str) -> str:
            while True:
                date_str = Prompt.ask(prompt_text)
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    return date_str
                except ValueError:
                    console.print("Invalid date format. Please enter the date in YYYY-MM-DD format.", style="bold red")

        start_date = get_valid_date("Enter start date (YYYY-MM-DD)")
        end_date = get_valid_date("Enter end date (YYYY-MM-DD)")

        activities = api.get_activities_by_date(start_date, end_date)

        if activities:
            viewer = DataViewer(activities)
            viewer.view_data()
        else:
            console.print(f"No activities found between {start_date} and {end_date}.", style="bold yellow")
    
        return activities