from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.syntax import Syntax
import json

class DataViewer:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.console = Console()

    def view_data(self) -> None:
        for i, activity in enumerate(self.data, 1):
            self.console.print(Panel(f"[bold cyan]Activity {i}[/bold cyan]", expand=False))
            
            # Create a table for basic activity info
            table = Table(title="Activity Summary")
            table.add_column("Attribute", style="cyan")
            table.add_column("Value", style="magenta")
            
            basic_info = [
                ("Activity Name", activity.get('activityName', 'N/A')),
                ("Activity Type", activity.get('activityType', {}).get('typeKey', 'N/A')),
                ("Start Time", activity.get('startTimeLocal', 'N/A')),
                ("Duration", f"{activity.get('duration', 0) / 60:.2f} minutes"),
                ("Distance", f"{activity.get('distance', 0) / 1000:.2f} km"),
                ("Average Speed", f"{activity.get('averageSpeed', 0) * 3.6:.2f} km/h"),
            ]
            
            for attr, value in basic_info:
                table.add_row(attr, str(value))
            
            self.console.print(table)
            
            # Create a tree for detailed data
            tree = Tree("[bold green]Detailed Data[/bold green]")
            self._add_dict_to_tree(activity, tree)
            
            self.console.print(tree)
            self.console.print("\n" + "="*50 + "\n")

    def _add_dict_to_tree(self, data: Dict[str, Any], tree: Tree, max_depth: int = 2, current_depth: int = 0):
        if current_depth >= max_depth:
            return

        for key, value in data.items():
            if isinstance(value, dict):
                branch = tree.add(f"[bold blue]{key}[/bold blue]")
                self._add_dict_to_tree(value, branch, max_depth, current_depth + 1)
            elif isinstance(value, list):
                branch = tree.add(f"[bold blue]{key}[/bold blue] (list with {len(value)} items)")
                if len(value) > 0 and isinstance(value[0], dict):
                    self._add_dict_to_tree(value[0], branch, max_depth, current_depth + 1)
            else:
                tree.add(Text(f"{key}: ", "yellow") + Text(str(value), "green"))
    @staticmethod
    def display_rich_output(api_call: str, output: Any) -> None:
        console = Console()
        console.print(Panel(api_call, border_style="bold cyan"))
        
        if isinstance(output, (dict, list)):
            json_str = json.dumps(output, indent=2)
            syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
            console.print(syntax)
        else:
            console.print(str(output))

# Example usage:
if __name__ == "__main__":
    # Sample data (replace with actual data from Garmin Connect)
    sample_data = [
        {
            "activityName": "Morning Run",
            "activityType": {"typeKey": "running"},
            "startTimeLocal": "2024-09-15 07:30:00",
            "duration": 1800,  # in seconds
            "distance": 5000,  # in meters
            "averageSpeed": 2.78,  # in m/s
            "elevationGain": 50,
            "averageHeartRate": 140,
            "maxHeartRate": 165,
            "calories": 300,
            "weather": {
                "temperature": 20,
                "humidity": 65,
                "windSpeed": 5
            }
        }
    ]

    viewer = DataViewer(sample_data)
    viewer.view_data()