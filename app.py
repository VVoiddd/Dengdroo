import os
import sys
import time
import subprocess
from colorama import init, Fore
from Private import temp_file_cleaner, memory_optimizer, disk_cleaner, startup_optimizer

init(autoreset=True)
GITHUB_REPO_URL = "https://github.com/Rooshyy/Dengdro.git"

CURRENT_VERSION = "1.0.0"
LATEST_VERSION = "1.1.0"
CHANGELOG = {
    "1.1.0": ["Added new optimization feature", "Fixed minor bugs"]
}

def fetch_latest_from_github():
    """Attempt to fetch the latest changes from GitHub."""
    try:
        result = subprocess.run(["git", "pull", GITHUB_REPO_URL], capture_output=True, text=True, check=True)
        if "Already up to date." in result.stdout:
            return False  # No updates found
        else:
            return True  # There were some updates
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error while checking for updates. Please ensure git is installed and your repo is correctly set up.")
        return False

def check_for_updates():
    return CURRENT_VERSION != LATEST_VERSION

def update_application():
    global CURRENT_VERSION
    CURRENT_VERSION = LATEST_VERSION
    with open("update_log.txt", "a") as log:
        log.write(f"Updated to version {LATEST_VERSION}\n")
        for change in CHANGELOG[LATEST_VERSION]:
            log.write(f"- {change}\n")
        log.write("\n")

def center_text(text, width=80):
    for line in text.split('\n'):
        print(line.center(width))

def loading_animation(duration=3):
    end_time = time.time() + duration
    symbols = ["◢", "◣", "◤", "◥"]

    while time.time() < end_time:
        for symbol in symbols:
            sys.stdout.write('\r' + f'Loading {symbol}')
            sys.stdout.flush()
            time.sleep(0.2)
    sys.stdout.write('\r' + ' ' * 15)
    sys.stdout.flush()

def display_colored_logo():
    colors = [Fore.RED, Fore.GREEN]
    for index, line in enumerate(LOGO.strip().split('\n')):
        print(colors[index % 2] + line.center(80))

LOGO = '''
________                         ____       .___                   
\______ \     ____     ____     / ___\    __| _/ _______    ____   
 |    |  \  _/ __ \   /    \   / /_/  >  / __ |  \_  __ \  /  _ \  
 |    `   \ \  ___/  |   |  \  \___  /  / /_/ |   |  | \/ (  <_> ) 
/_______  /  \___  > |___|  / /_____/   \____ |   |__|     \____/  
        \/       \/       \/                 \/                    
'''

MENU_OPTIONS = {
    "1": ("Clear Temp Files", temp_file_cleaner.clean_temp_files),
    "2": ("Optimize Memory", memory_optimizer.optimize_memory),
    "3": ("Clean Disk", disk_cleaner.clean_disk),
    "4": ("List Startup Programs", startup_optimizer.list_startup_programs),
}

def display_menu():
    menu = [f"{Fore.LIGHTBLACK_EX}{key}. {value[0]}" for key, value in MENU_OPTIONS.items()]
    menu.append(f"{Fore.LIGHTBLACK_EX}5. Exit")
    center_text("\n".join(menu))

def main():
    # Check for GitHub updates at the start of the application.
    should_check_github = input("Do you want to check for updates on GitHub? (Y/N): ").lower()
    if should_check_github == 'y':
        if fetch_latest_from_github():
            print(f"{Fore.GREEN}Updates were fetched from GitHub! Please restart the application to see the changes.")
            sys.exit(0)
        else:
            print(f"{Fore.LIGHTBLACK_EX}Your application is already up-to-date!")

    # Check for internal version updates
    if check_for_updates():
        should_update = input("New internal updates are available. Do you want to update now? (Y/N): ").lower()
        if should_update == 'y':
            update_application()
            print(f"{Fore.LIGHTBLACK_EX}Application updated to version {LATEST_VERSION}!")
            input("\nPress enter to continue...")
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_colored_logo()
        display_menu()
        
        choice = input("\nEnter your choice: ")

        if choice in MENU_OPTIONS:
            loading_animation()
            MENU_OPTIONS[choice][1]()
        elif choice == "5":
            print(f"{Fore.RED}Exiting Dengdro...")
            break
        else:
            print(f"{Fore.LIGHTBLACK_EX}Invalid choice. Please select a valid option.")

        input("\nPress enter to return to the main menu...")

if __name__ == "__main__":
    main()
