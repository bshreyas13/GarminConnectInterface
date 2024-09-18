# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 12:34:56 2024
Summary: This is an interface for interacting with the Garmin Connect API, allowing users to retrieve and display various fitness data.
Author: github.com/bshreyas13
"""

import logging
from typing import Dict, Callable
from modules.menu import Menu
from modules.client import GarminConnectClient
from plugins.base_plugin import BasePlugin
import importlib
import os
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
    def __init__(self, email: str, password: str):
        self.api_client = GarminConnectClient(email, password)
        self.menu = Menu()
        self.commands: Dict[str, Callable] = {}
        self.plugins: Dict[str, BasePlugin] = {}
        self._load_plugins()
        self._setup_menu()

    def _load_plugins(self):
        plugin_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'plugins')
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and filename != 'base_plugin.py':
                module_name = filename[:-3]  # Remove .py extension
                module = importlib.import_module(f'plugins.{module_name}')
                for item in dir(module):
                    item = getattr(module, item)
                    if isinstance(item, type) and issubclass(item, BasePlugin) and item != BasePlugin:
                        plugin = item()
                        self.plugins[plugin.command_key] = plugin

    def _setup_menu(self):
        sorted_keys = sorted(self.plugins.keys(), key=lambda k: (0, int(k)) if k.isdigit() else (1, k))
        for key in sorted_keys:
            plugin = self.plugins[key]
            self.menu.add_option(key, plugin.description)
            self.commands[key] = plugin.execute

        # Add exit options
        self.menu.add_option("q", "Exit without logging out")
        self.menu.add_option("Q", "Log session out and exit")

    def run(self):
        while True:
            console.print(Panel.fit("Garmin Connect API Demo. Author:bshreyas13", border_style="bold green"))
            
            if not self.api_client.api:
                if not self.api_client.login():
                    console.print(Panel.fit("Could not login to Garmin Connect, try again later.", border_style="bold_red", style="bold red"))
                    break

            self.menu.display()
            option = self.menu.get_selection()

            if option == "q":
                console.print(Panel.fit("Exiting the program without logging out session. Goodbye!", border_style="yellow", style="bold blue"))
                break
            elif option == "Q":
                self.api_client.logout()
                console.print(Panel.fit("Logged out successfully. Goodbye!", border_style="bold blue", style="bold blue"))
                break

            try:
                command_func = self.commands.get(option)
                if command_func:
                    command_func(self.api_client.api)
                else:
                    console.print(f"Command '{option}' not found.", style="bold red")
                
            except Exception as err:
                logger.error(err)
                console.print(f"Error: {err}", style="bold red")



class CredentialsManager:
    """
    Manages user credentials using the keyring library for secure storage.

    Attributes:
        KEYRING_SERVICE (str): The name of the keyring service used for storing credentials.
        email (str): The user's email address.
        password (str): The user's password.
    """

    KEYRING_SERVICE = "GarminConnect"

    def __init__(self):
        """
        Initializes the CredentialsManager with email and password set to None.
        """
        self.email = None
        self.password = None

    def get_credentials(self):
        """
        Retrieves the user's credentials from the keyring or prompts the user to enter them.

        This method first attempts to retrieve the email and password from the keyring. If the
        credentials are not found or there is an error accessing the keyring, it prompts the user
        to enter their email and password. The entered credentials are then stored in the keyring.

        Returns:
            tuple: A tuple containing the email and password.
        """
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
        """
        Deletes the stored credentials from the keyring.

        This method attempts to delete the email and password from the keyring. If there is an error
        during the deletion process, it logs the error and notifies the user.

        """
        KEYRING_SERVICE = "GarminConnect"
        try:
            keyring.delete_password(KEYRING_SERVICE, "email")
            keyring.delete_password(KEYRING_SERVICE, "password")
            console.print("Stored credentials have been deleted.", style="bold green")
        except keyring.errors.KeyringError as e:
            logger.error(f"Error deleting credentials from keyring: {e}")
            console.print("Could not delete credentials.", style="bold red")