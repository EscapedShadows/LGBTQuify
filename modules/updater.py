import requests
from packaging.version import Version

def updater(local):
    local_version = Version(local)
    github_version = Version(requests.get("https://raw.githubusercontent.com/EscapedShadows/LGBTQuify/refs/heads/main/version.txt").text)

    if github_version > local_version:
        print("="*10)
        print("Update available!")
        print("="*10)
        install = input("Would you like to install the update? (y/n): ")
        install = True if install.lower() == "y" else False

        return install