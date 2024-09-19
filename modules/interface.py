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
from modules.credentials_manager import CredentialsManager
import traceback
from plugins.plugin_types import PluginType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

class GarminConnectInterface:
    def __init__(self, credentials_manager: CredentialsManager):
        self.credentials_manager = credentials_manager
        email, password = self.credentials_manager.get_credentials()
        self.api_client = GarminConnectClient(email, password)
        self.menu = Menu()
        self.commands: Dict[str, Callable] = {}
        self.plugins: Dict[str, BasePlugin] = {}
        self.retrieval_plugins: list = []
        self.process_plugins:list = []
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
            if plugin.plugin_type == PluginType.DATA_RETRIEVAL:
                self.retrieval_plugins.append(key)
            elif plugin.plugin_type == PluginType.DATA_PROCESSING:
                self.process_plugins.append(key)
            self.commands[key] = plugin.execute
            
        # Add exit options
        self.menu.add_option("q", "Exit without logging out")
        self.menu.add_option("Q", "Log session out and exit")

    def run(self):
        while True:
            console.print(Panel.fit("Garmin Connect API Demo. Author:bshreyas13", border_style="bold green"))
            
            if not self.api_client.api:
                if not self.api_client.login():
                    
                    console.print(Panel.fit("Could not login to Garmin Connect, invalid credentials.", border_style="bold red", style="bold red"))
                    self.credentials_manager.delete_credentials()
                    break

            self.menu.display()
            option = self.menu.get_selection()

            if option == "q":
                console.print(Panel.fit("Exiting the program without logging out session. Goodbye!", border_style="yellow", style="bold blue"))
                
                break
            elif option == "Q":
                self.api_client.logout()
                self.credentials_manager.delete_credentials()
                console.print(Panel.fit("Logged out successfully. Goodbye!", border_style="bold blue", style="bold blue"))
                break

            try:
                command_func = self.commands.get(option)
                if command_func is None:
                    console.print(f"Command '{option}' not found.", style="bold red")
                    continue
                
                if option in self.retrieval_plugins :
                   command_func(self.api_client.api)
                
                if option in self.process_plugins :
                    ret_func = self.commands.get('R')
                    data = ret_func(self.api_client.api, display=False) 
                    merged_data = command_func(self.api_client.api, data)
                    print(len(merged_data))
                    print(merged_data[0]["geoPolylineDTO"]["polyline"][:5])

            except Exception as err:
                logger.error(err)
                console.print(f"Error: {traceback.format_exc()}", style="bold red")



