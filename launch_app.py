# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 12:34:56 2024
Summary: Terminal App for using Garmin connect API.
Author: github.com/bshreyas13
"""
import logging
from modules.menu import Menu
from modules.interface import GarminConnectInterface, CredentialsManager
from rich.console import Console

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


if __name__ == "__main__":
    creds = CredentialsManager()

    email, password = creds.get_credentials()

    demo = GarminConnectInterface(email, password)
    demo.run()
