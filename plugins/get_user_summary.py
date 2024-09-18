
from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
import datetime

class GetUserSummaryPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "4"

    @property
    def description(self) -> str:
        return "Get User Summary"

    def execute(self, api):
        today = datetime.date.today()
        user_summary = api.get_user_summary(today.isoformat())
        DataViewer.display_rich_output("User Summary:", user_summary)
        return user_summary