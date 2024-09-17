# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 12:34:56 2024
Summary: This is an interface for interacting with the Garmin Connect API, allowing users to retrieve and display various fitness data.
Author: github.com/bshreyas13
"""

import logging
from typing import Dict, Callable
from modules.data_accesspoints import (
    get_full_name,
    get_unit_system,
    get_stats,
    get_user_summary,
    get_body_composition,
    get_last_ten_activities,
    get_last_activity,
    get_devices,
    get_active_goals,
    get_hrv_data,
    get_activity_for_range,
    display_method_docstrings,
    merge_activities,
)
from modules.menu import Menu
from modules.client import GarminConnectClient
import requests
from garth.exc import GarthHTTPError
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import keyring
from keyring.errors import KeyringError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


class GarminConnectInterface:
    """
    GarminConnectInterface class represents an interface for interacting with the Garmin Connect API.
    Attributes:
        api_client (GarminConnectClient): The client for the Garmin Connect API.
        menu (Menu): The menu object for displaying options.
        commands (Dict[str, Callable[[Garmin], None]]): A dictionary mapping option strings to command functions.
    Methods:
        __init__(self, email: str, password: str): Initializes the GarminConnectInterface object.
        _setup_menu(self) -> None: Sets up the menu options.
        _setup_commands(self) -> None: Sets up the command functions.
        run(self) -> None: Runs the interface loop.
    """
    def __init__(self, email: str, password: str):
        self.api_client = GarminConnectClient(email, password)
        self.menu = Menu()
        self.commands: Dict[str, Callable[[Garmin], None]] = {}
        self._setup_menu()
        self._setup_commands()

    def _setup_menu(self) -> None:
        self.menu.add_option("1", "Get full name")
        self.menu.add_option("2", "Get unit system")
        self.menu.add_option("3", "Get activity data for today")
        self.menu.add_option("4", "Get activity data for today (compatible with garminconnect-ha)")
        self.menu.add_option("5", "Get body composition data for today")
        self.menu.add_option("6", "Get last 10 activities")
        self.menu.add_option("7", "Get last activity")
        self.menu.add_option("8", "Get Garmin devices")
        self.menu.add_option("9", "Get active goals")
        self.menu.add_option("0", "Get HRV data for today")
        self.menu.add_option("R", "Get activity data for a date range")
        self.menu.add_option("M", "Merge activities")
        self.menu.add_option("q", "Exit without logging out")
        self.menu.add_option("Q", "Log session out and exit")
        self.menu.add_option("H", "(Dev options) Display all available methods in Garmin API with docstrings")


    def _setup_commands(self) -> None:
        self.commands = {
            "1": get_full_name,
            "2": get_unit_system,
            "3": get_stats,
            "4": get_user_summary,
            "5": get_body_composition,
            "6": get_last_ten_activities,
            "7": get_last_activity,
            "8": get_devices,
            "9": get_active_goals,
            "0": get_hrv_data,
            "H": display_method_docstrings,
            "R": get_activity_for_range,
            "M": merge_activities,
        }

    def run(self) -> None:
        while True:
            console.print(Panel.fit("Garmin Connect API Demo. Author:bshreyas13", border_style="bold green"))
            
            if not self.api_client.api:
                if not self.api_client.login():
                    console.print("Could not login to Garmin Connect, try again later.", style="bold red")
                    break

            self.menu.display()
            option = self.menu.get_selection()

            if option == "q":
                console.print("Exiting the program without logging out session. Goodbye!", style="bold blue")
                break
            elif option == "Q":
                self.api_client.logout()
                CredentialsManager().delete_credentials()
                console.print("Logged out successfully. Goodbye!", style="bold blue")
                break

            try:
                command_func = self.commands.get(option)
                if command_func:
                    command_func(self.api_client.api)
                else:
                    console.print(f"Command '{option}' not found.", style="bold red")
                
            except (
                GarminConnectConnectionError,
                GarminConnectAuthenticationError,
                GarminConnectTooManyRequestsError,
                requests.exceptions.HTTPError,
                GarthHTTPError
            ) as err:
                logger.error(err)
                console.print(f"Error: {err}", style="bold red")
        

class CredentialsManager:
    KEYRING_SERVICE = "GarminConnect"

    def __init__(self):
        self.email = None
        self.password = None

    def get_credentials(self):
        try:
            # Try to get email and password from keyring
            self.email = keyring.get_password(self.KEYRING_SERVICE, "email")
            self.password = keyring.get_password(self.KEYRING_SERVICE, "password")
        except KeyringError as e:
            logger.error(f"Error accessing keyring: {e}")
            self.email = None
            self.password = None

        if not self.email or not self.password:
            self.email = Prompt.ask("Login e-mail")
            self.password = Prompt.ask("Enter password", password=True)

            # Store the credentials in keyring
            try:
                keyring.set_password(self.KEYRING_SERVICE, "email", self.email)
                keyring.set_password(self.KEYRING_SERVICE, "password", self.password)
            except KeyringError as e:
                logger.error(f"Error storing credentials in keyring: {e}")
                console.print("Could not store credentials securely. Proceeding without storing.")

        return self.email, self.password
    
    def delete_credentials(self):
        KEYRING_SERVICE = "GarminConnect"
        try:
            keyring.delete_password(KEYRING_SERVICE, "email")
            keyring.delete_password(KEYRING_SERVICE, "password")
            console.print("Stored credentials have been deleted.", style="bold green")
        except keyring.errors.KeyringError as e:
            logger.error(f"Error deleting credentials from keyring: {e}")
            console.print("Could not delete credentials.", style="bold red")
