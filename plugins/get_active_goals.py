from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer

class GetActiveGoalsPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "9"

    @property
    def description(self) -> str:
        return "Get active goals"

    def execute(self, api):
        active_goals = api.get_goals("active")
        DataViewer.display_rich_output("Active Goals:", active_goals)
        return active_goals