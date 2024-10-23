import subprocess
import sys

class PackageChecker:
    def __init__(self, required_packages):
        """
        Initialize with a list of required packages.
        """
        self.required_packages = required_packages
        self.installed_packages = self.list_installed_packages()

    def list_installed_packages(self):
        """
        Use pip to list all installed packages.
        Returns a list of installed package names.
        """
        try:
            result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                # Split the output into lines and extract package names (skipping headers)
                packages = [line.split()[0].lower() for line in result.stdout.split('\n')[2:] if line]
                return packages
            else:
                print(f"Error fetching installed packages: {result.stderr}")
                return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def check_missing_packages(self):
        """
        Check for missing packages by comparing installed packages with required ones.
        Returns a list of missing packages.
        """
        return [pkg for pkg in self.required_packages if pkg.lower() not in self.installed_packages]

    def install_packages(self, packages):
        """
        Install the provided list of packages using pip with the --break-system-packages flag.
        """
        for pkg in packages:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--break-system-packages"])

    def ensure_packages(self):
        """
        Check for missing packages and install them if needed.
        """
        missing_packages = self.check_missing_packages()
        if not missing_packages:
            print("All required packages are installed!")
        else:
            print("Missing packages found. Installing...")
            self.install_packages(missing_packages)
            print("All required packages are now installed!")

required = ["requests", "colorama", "InquirerPy", "packaging"]
checker = PackageChecker(required)
checker.ensure_packages()

import os
import requests
from colorama import Fore, init
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import time
import shutil
import json
from json import JSONDecodeError

init(autoreset=True)

class Settings:
    def __init__(self):
        """
        Initialize the Settings object and load settings from the JSON file.
        """
        self.reload()

    def write_settings(self):
        """
        Save the current settings to the JSON file.
        """
        settings = self.settings  # Get the current settings
        with open("settings.json", "w") as f:  # Open file for writing
            json.dump(settings, f, indent=4)  # Write settings in JSON format

    def reload(self):
        """
        Load settings from the JSON file.
        If the file doesn't exist or contains invalid JSON, initialize an empty settings dictionary.
        """
        with open("settings.json", "r") as f:  # Open file for reading
            try:
                settings = json.load(f)  # Load settings from JSON
            except json.JSONDecodeError:  # Handle JSON errors
                settings = {}  # Set settings to an empty dictionary on error
        self.settings = settings  # Store the loaded settings

    def set_setting(self, setting):
        """
        Update a specific setting with the given key and value, and save changes.
        """
        settings = self.settings  # Get current settings
        settings[setting["key"]] = setting["value"]  # Update the setting
        self.write_settings()  # Save updated settings

    def get_setting(self, setting):
        """
        Retrieve the value of a specific setting by key.
        Returns None if the setting does not exist.
        """
        return self.settings.get(setting, None)  # Return the setting value or None

class LGBTQUifyUpdater:
    def __init__(self, base_url):
        self.base_url = base_url

    def fatal_error(self, message, error):
        """Prints the error message and exits the program."""
        print(f"{Fore.RED}Fatal Error: {message}")
        print(f"{Fore.RED}Error Details: {error}")
        print(f"{Fore.YELLOW}Please report this error with the details above.")
        sys.exit(1)

    def get_index_file(self, url):
        """Fetches the index file from the given URL."""
        try:
            print("="*30)
            print(f"{Fore.YELLOW}Fetching index file...")
            print("="*30)
            response = requests.get(url)
            response.raise_for_status()
            print(f"{Fore.GREEN}Index file downloaded successfully.\n")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.fatal_error("Failed to download index file", e)

    def create_folders(self, index):
        """Creates the necessary folders based on the index file."""
        print("="*30)
        print(f"{Fore.YELLOW}Creating folders...")
        print("="*30)
        for folder_path in index["folders"]:
            try:
                os.makedirs(folder_path, exist_ok=True)
                print(f"{Fore.GREEN}Folder '{folder_path}' created successfully.\n")
            except OSError as e:
                self.fatal_error(f"Error creating folder '{folder_path}'", e)

    def download_file(self, url, file_path):
        """Downloads and saves a file from the given URL."""
        try:
            print(f"{Fore.YELLOW}Downloading file: {file_path}")
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"{Fore.GREEN}File {file_path} downloaded successfully.\n")
        except requests.exceptions.RequestException as e:
            self.fatal_error(f"Error downloading {file_path}", e)
        except OSError as e:
            self.fatal_error(f"Error writing to {file_path}", e)

    def download_files(self, index):
        """Downloads all the files listed in the index."""
        print("="*30)
        print(f"{Fore.YELLOW}Downloading files...")
        print("="*30)
        for file_path in index["files"]:
            file_url = self.base_url + file_path
            self.download_file(file_url, file_path)

    def run_update(self, index_url):
        """Runs the entire update process."""
        index = self.get_index_file(index_url)
        self.create_folders(index)
        self.download_files(index)

if __name__ == "__main__":
    """
    Version / Update checking
    """
    updater = LGBTQUifyUpdater(base_url="https://raw.githubusercontent.com/EscapedShadows/LGBTQuify/refs/heads/main/")
    
    if not os.path.isfile("version.txt"):
        index_url = updater.base_url + "index.json"
        updater.run_update(index_url)
    else:
        index_url = updater.base_url + "index.json"
        from modules.version import version
        with open("version.txt", "r") as file:
            local_version = file.read().strip()
        file.close()

        ORANGE = '\033[38;5;214m'
        PURPLE = '\033[38;5;129m'

        print(f"{Fore.YELLOW}Getting latest version from GitHub...")

        update = version(local_version)
        updater.run_update(index_url) if update else None
        print(f"{Fore.RED}L{ORANGE}G{Fore.YELLOW}B{Fore.GREEN}T{Fore.BLUE}Q{PURPLE}u{Fore.RED}i{ORANGE}f{Fore.YELLOW}y {Fore.GREEN}is up to date. Current version: {local_version}\n") if update is None else None
        time.sleep(1)

    """
    Actions
    """
    
    #os.system("cls") if os.name == "nt" else os.system("clear")

    action = inquirer.select(
        message="Select an action:",
        choices=[
            "LGBTQuify",
            "Repair",
            "Uninstall",
            Separator(),
            Choice(value=None, name="Exit")
        ],
    ).execute()

    exit(0) if action == None else None

    if action == "Repair":
        updater = LGBTQUifyUpdater(base_url="https://raw.githubusercontent.com/EscapedShadows/LGBTQuify/refs/heads/main/")
        index_url = updater.base_url + "index.json"
        updater.run_update(index_url)
        exit()
    
    if action == "Uninstall":
        files = [
            "LICENSE",
            "README.md",
            "version.txt"
        ]
        folders = [
            "modules",
            "static",
            "scripts",
            "flags",
            "ascii"
        ]

        for file in files:
            try:
                print(f"{Fore.YELLOW}Removing {file}")
                os.remove(file)
                print(f"{Fore.GREEN}Removed {file}")
            except OSError as e:
                updater.fatal_error(f"Failed to delete {file}", e)
                exit(1)

        for folder in folders:
            try:
                print(f"{Fore.YELLOW}Removing {folder}")
                shutil.rmtree(folder)
                print(f"{Fore.GREEN}Removed {folder}")
            except OSError as e:
                updater.fatal_error(f"Failed to delete {file}", e)
                exit(1)
        exit(0)

    from static.flags import flags
    from modules.change_flags import FlagChanger

    settings = Settings()

    available_flags = flags

    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Change Flag(s)",
            "Apply Flag(s)",
            "Remove",
            Separator(),
            Choice(value=None, name="Exit")
        ],
    ).execute()

    if action == "Change Flag(s)":
        flag_changer = FlagChanger(flags, settings)
        flag_changer.select_flags()