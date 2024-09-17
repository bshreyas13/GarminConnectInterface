import requests
from garth.exc import GarthHTTPError
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
)
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

class GarminConnectClient:
    """
    A client for interacting with the Garmin Connect API.
    Args:
        email (str): The email address associated with the Garmin Connect account.
        password (str): The password for the Garmin Connect account.
    Attributes:
        email (str): The email address associated with the Garmin Connect account.
        password (str): The password for the Garmin Connect account.
        api (Garmin): The Garmin API client.
        tokenstore (str): The path to the directory where login tokens are stored.
    Methods:
        login(): Logs in to Garmin Connect using token data or credentials.
        logout(): Logs out of Garmin Connect and removes stored login tokens.
    """
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.api = None
        self.tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"

    def login(self):
        """
        Logs in to Garmin Connect using token data or credentials.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        try:
            console.print(f"Trying to login to Garmin Connect using token data from directory '{self.tokenstore}'...\n")
            self.api = Garmin()
            self.api.login(self.tokenstore)
        except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
            console.print(f"Login tokens not present, logging in with credentials.\n")
            try:
                self.api = Garmin(email=self.email, password=self.password)
                self.api.login()
                self.api.garth.dump(self.tokenstore)
                console.print(f"Oauth tokens stored in '{self.tokenstore}' directory for future use.\n")
            except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError, requests.exceptions.HTTPError) as err:
                logger.error(err)
                return False
        return True

    def logout(self):
        """
        Logs out the user and removes stored login tokens.
        This method removes any stored login tokens from the specified token directory.
        It also calls the `logout` method of the API object to log out the user.
        After calling this method, the API object is set to `None`.
        Raises:
            FileNotFoundError: If the token directory is not found.
        """
        # Rest of the code...

        tokendir = os.path.expanduser(self.tokenstore)
        console.print(f"Removing stored login tokens from: {tokendir}")
        try:
            for root, dirs, files in os.walk(tokendir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            console.print(f"Directory {tokendir} removed")
            
        except FileNotFoundError:
            console.print(f"Directory not found: {tokendir}")
        self.api = None

