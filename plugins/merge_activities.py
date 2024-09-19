from plugins.base_plugin import BasePlugin
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from modules.data_viewer import DataViewer
from plugins.plugin_types import PluginType
from enum import Enum

console = Console()


class MergeActivitiesPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "M"

    @property
    def description(self) -> str:
        return "Merge activities. (Type of activities need to be same in the current implementation)"
    @property
    def plugin_type(self) -> Enum:
        return PluginType.DATA_PROCESSING
    
    def execute(self, api, activities,display=True):
        
        activity_ids = [a.get("activityId") for a in activities]
        if display:
            DataViewer.display_rich_output(f"Found {len(activities)} activities with listed Ids", activity_ids)
        
        merged_data = [ api.get_activity_details(activity_id) for activity_id in activity_ids]
        
        activity_details = api.get_activity_details(activity_ids[-1])
            
        if display:
            DataViewer.display_rich_output(f"Details avaialable for each activity:", list(activity_details.keys()))
            
        console.print(Panel.fit(f"Merged activity details for {len(activities)} activities.", border_style= 'green', style="bold Green"))
        return merged_data