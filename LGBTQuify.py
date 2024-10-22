import os
import sys
import requests
from colorama import Fore, init
from InquirerPy import prompt, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import time
import shutil

init(autoreset=True)

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

        for folder in folders:
            try:
                print(f"{Fore.YELLOW}Removing {folder}")
                shutil.rmtree(folder)
                print(f"{Fore.GREEN}Removed {folder}")
            except OSError as e:
                updater.fatal_error(f"Failed to delete {file}", e)