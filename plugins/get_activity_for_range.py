from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
from rich.console import Console
from rich.prompt import Prompt
from datetime import datetime
from plugins.plugin_types import PluginType
from enum import Enum

console = Console()

class GetActivityForRangePlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "R"

    @property
    def description(self) -> str:
        return "Get activity data for a date range"

    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_RETRIEVAL
    
    def execute(self, api, display=True):
        def get_valid_date(prompt_text: str, start_date_:str = None) -> str:
            while True:
                if 'end date' in prompt_text.lower() and start_date_:
                    date_str = Prompt.ask(prompt_text, default=start_date_)
                else:
                    date_str = Prompt.ask(prompt_text)
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    return date_str
                except ValueError:
                    console.print("Invalid date format. Please enter the date in YYYY-MM-DD format.", style="bold red")

        start_date = get_valid_date("Enter start date (YYYY-MM-DD)")
        end_date = get_valid_date("Enter end date (YYYY-MM-DD) (Optional). Default is start date", start_date)
        activity_type = Prompt.ask("Enter activity type (optional)", default=None)

        if activity_type is None:
            activities = api.get_activities_by_date(start_date, end_date)            
        else:
            activities = api.get_activities_by_date(start_date, end_date, activity_type)

        if not activities:
            console.print("No activities found for the given date range.", style="bold yellow")
            return []
        
        if display:
            viewer = DataViewer(activities)
            viewer.view_data()
        
        
        return activities