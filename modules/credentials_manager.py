from rich.prompt import Prompt
import keyring
from keyring.errors import KeyringError
from rich.console import Console
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

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