import requests
from packaging.version import Version
from colorama import Fore, init

init(autoreset=True)

def version(local):
    local_version = Version(local)
    github_version = Version(requests.get("https://raw.githubusercontent.com/EscapedShadows/LGBTQuify/refs/heads/main/version.txt").text)

    if github_version > local_version:
        print("="*10)
        print(f"{Fore.GREEN}Update available!")
        print("="*10)
        install = input(f"{Fore.YELLOW}Would you like to install the update? (y/n): ")
        install = True if install.lower() == "y" else False

        return install
    return None