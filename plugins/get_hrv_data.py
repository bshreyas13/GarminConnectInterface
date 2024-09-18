from plugins.base_plugin import BasePlugin
from modules.data_viewer import DataViewer
import datetime

class GetHRVDataPlugin(BasePlugin):
    @property
    def command_key(self) -> str:
        return "8"

    @property
    def description(self) -> str:
        return "Get HRV data for today"

    def execute(self, api):
        today = datetime.date.today()
        hrv_data = api.get_hrv_data(today.isoformat())
        DataViewer.display_rich_output("HRV Data:", hrv_data)
        return hrv_data
    
