from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from modules.data_viewer import DataViewer
from garminconnect import Garmin
import datetime

console = Console()

# Command functions
def get_full_name(api: Garmin) -> None:
    full_name = api.get_full_name()
    DataViewer.display_rich_output("Full Name:", full_name)

def get_unit_system(api: Garmin) -> None:
    unit_system = api.get_unit_system()
    DataViewer.display_rich_output("Unit System:", unit_system)

def get_stats(api: Garmin) -> None:
    today = datetime.date.today()
    stats = api.get_stats(today.isoformat())
    DataViewer.display_rich_output("Stats:", stats)

def get_user_summary(api: Garmin) -> None:
    today = datetime.date.today()
    user_summary = api.get_user_summary(today.isoformat())
    DataViewer.display_rich_output("User Summary:", user_summary)

def get_body_composition(api: Garmin) -> None:
    today = datetime.date.today()
    body_composition = api.get_body_composition(today.isoformat())
    DataViewer.display_rich_output("Body Composition:", body_composition)

def get_last_ten_activities(api: Garmin) -> None:
    last_ten_activities = api.get_activities(0, 10)
    if last_ten_activities:
        viewer = DataViewer(last_ten_activities)
        viewer.view_data()
    else:
        console.print(f"No activities found.", style="bold yellow")

def get_last_activity(api: Garmin) -> None:
    last_activity = api.get_last_activity()
    if last_activity:
        # Use DataViewer to display the activities
        viewer = DataViewer([last_activity])
        viewer.view_data()
    else:
        console.print(f"No last activity found.", style="bold yellow")

def get_devices(api: Garmin) -> None:
    devices = api.get_devices()
    DataViewer.display_rich_output("Devices:", devices)

def get_active_goals(api: Garmin) -> None:
    active_goals = api.get_goals("active")
    DataViewer.display_rich_output("Active Goals:", active_goals)

def get_hrv_data(api: Garmin) -> None:
    today = datetime.date.today()
    hrv_data = api.get_hrv_data(today.isoformat())
    DataViewer.display_rich_output("HRV Data:", hrv_data)

def get_activity_for_range(api: Garmin) -> None:
    from datetime import datetime

    def get_valid_date(prompt_text: str) -> str:
        while True:
            date_str = Prompt.ask(prompt_text)
            try:
                # Validate the date format
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                console.print("Invalid date format. Please enter the date in YYYY-MM-DD format.", style="bold red")

    start_date = get_valid_date("Enter start date (YYYY-MM-DD)")
    end_date = get_valid_date("Enter end date (YYYY-MM-DD)")

    # Fetch activities for the date range
    activities = api.get_activities_by_date(start_date, end_date)

    if activities:
        # Use DataViewer to display the activities
        viewer = DataViewer(activities)
        viewer.view_data()
    else:
        console.print(f"No activities found between {start_date} and {end_date}.", style="bold yellow")

def display_method_docstrings(api: Garmin) -> None:
    table = Table(title="Garmin Connect API Methods", show_header=True, header_style="bold magenta")
    table.add_column("Method", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")

    methods = [method for method in dir(api) if callable(getattr(api, method)) and not method.startswith("_")]
    
    for method in sorted(methods):
        doc = getattr(api, method).__doc__
        if doc:
            # Split the docstring into summary and details
            summary, *details = doc.strip().split('\n', 1)
            summary = summary.strip()
            details = '\n'.join(details).strip() if details else ""

            # Create a Text object for the description
            description = Text(summary)
            if details:
                description.append("\n\n" + details, style="dim")

            table.add_row(method, description)

    console.print(table)
    console.print("\nPress any key to continue...", style="bold yellow")
    input()