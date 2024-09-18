# Garmin Connect API Demo

## Description

This application is a command-line interface (CLI) for interacting with the Garmin Connect API. It allows users to retrieve and display various fitness data from their Garmin Connect account, such as activity summaries, body composition, device information, and more.

## Features

- Secure login to Garmin Connect using email and password
- Token-based authentication for subsequent logins
- Retrieval of various fitness data:
  - User's full name and unit system
  - Activity data (daily stats, last 10 activities, specific date range)
  - Body composition data
  - Device information
  - Active goals
  - Heart Rate Variability (HRV) data
- Interactive menu for easy navigation
- Secure credential storage using system keyring
- Logging functionality for error tracking

## Prerequisites

- Python 3.7+
- Garmin Connect account

## Installation

### Local environment

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/garmin-connect-demo.git
   cd garmin-connect-demo
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Docker Method

This application is also available as a Docker container for easy deployment and use across different environments.

1. Pull the latest Docker image:
   ```bash
   docker pull bshreyas13/garminconnectinterface:latest
   ```

2. Run the Docker container:
   ```bash
   docker run -it -v /path/to/your/local/directory:/app bshreyas13/garminconnectinterface:latest
   ```
   
   Replace `/path/to/your/local/directory` with the path where you want to store or access data on your local machine.

   For example, on Windows using WSL, you might use:
   ```bash
   docker run -it -v /mnt/c/Users/yourusername/Documents/GarminConnectInterface/:/app bshreyas13/garminconnectinterface:latest
   ```

3. The application will start inside the Docker container, and you can interact with it as described in the usage section.

Note: Using the Docker method ensures that all dependencies are correctly installed and the environment is properly set up, regardless of your local system configuration.

## Usage

1. Run the launch script:
   ```
   python launch.py
   ```

2. If it's your first time running the app, you'll be prompted to enter your Garmin Connect email and password. These credentials will be securely stored for future use.

3. Use the interactive menu to select the data you want to retrieve. Enter the corresponding number or letter for your choice.

4. To exit the program, choose option 'q' to exit without logging out, or 'Q' to log out and exit.



## File Structure

- `launch.py`: The entry point of the application
- `interface.py`: The main interface logic
- `data_access_utils.py`: Utility functions for data retrieval and display
- `data_viewer.py`: Handles data display formatting
- `menu.py`: Manages the interactive menu
- `client.py`: Handles the Garmin Connect API client

## Security

- Credentials are securely stored using the system's keyring.
- OAuth tokens are stored locally for quicker subsequent logins.
- Option to log out and delete stored credentials is available.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is not affiliated with, endorsed by, or connected to Garmin Ltd. or its subsidiaries. Use it at your own risk and in compliance with Garmin's terms of service.

## Author

Created by github.com/bshreyas13

## Acknowledgments

- Thanks to the creators and maintainers of the `garminconnect` Python package.
- This project uses the `rich` library for enhanced CLI output.





