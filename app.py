import os
import sys
import time
import subprocess
from colorama import init, Fore
from Private import temp_file_cleaner, memory_optimizer, disk_cleaner, startup_optimizer

# Initialize colorama
init(autoreset=True)

# Constants
GITHUB_REPO_URL = "https://github.com/The-Only-Star/Dengdroo"
CURRENT_VERSION = "1.1.1"
CHANGELOG = {
    "1.0.0": ["Initial version"],
    "1.0.1": ["Added internal update checking"],
    "1.1.0": ["Integrated Git functionality to fetch updates from GitHub", "Improved error messaging for Git operations"],
    "1.1.1": ["Enhanced the loading animation with new symbols"]
}

def fetch_latest_from_github():
    """Attempt to fetch the latest changes from GitHub."""
    try:
        result = subprocess.run(["git", "pull", GITHUB_REPO_URL], capture_output=True, text=True, check=True)
        return "Already up to date." not in result.stdout
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error while checking for updates. Ensure git is installed and your repo is set up correctly.")
        return False

def is_new_version_available():
    """Check if a new internal version is available."""
    return CURRENT_VERSION != list(CHANGELOG.keys())[-1]

def display_update_log():
    """Display the changelog for the latest version."""
    latest_version = list(CHANGELOG.keys())[-1]
    print(f"{Fore.GREEN}Updated to version {latest_version}!")
    for change in CHANGELOG[latest_version]:
        print(f"- {change}")

def loading_animation(duration=3):
    """Display a rotating square as a loading animation."""
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
    logo = '''
________                         ____       .___                   
\______ \     ____     ____     / ___\    __| _/ _______    ____   
 |    |  \  _/ __ \   /    \   / /_/  >  / __ |  \_  __ \  /  _ \  
 |    `   \ \  ___/  |   |  \  \___  /  / /_/ |   |  | \/ (  <_> ) 
/_______  /  \___  > |___|  / /_____/   \____ |   |__|     \____/  
        \/       \/       \/                 \/                    
'''
    for index, line in enumerate(logo.strip().split('\n')):
        print(colors[index % 2] + line.center(80))

def display_menu():
    menu_options = {
        "1": ("Clear Temp Files", temp_file_cleaner.clean_temp_files),
        "2": ("Optimize Memory", memory_optimizer.optimize_memory),
        "3": ("Clean Disk", disk_cleaner.clean_disk),
        "4": ("List Startup Programs", startup_optimizer.list_startup_programs),
        "5": ("Exit", exit)
    }
    
    for key, value in menu_options.items():
        print(f"{Fore.LIGHTBLACK_EX}{key}. {value[0]}")

def main():
    # Check for GitHub updates
    should_check_github = input("Do you want to check for updates on GitHub? (Y/N): ").lower()
    if should_check_github == 'y':
        if fetch_latest_from_github():
            display_update_log()
            sys.exit(0)
        else:
            print(f"{Fore.LIGHTBLACK_EX}Your application is already up-to-date!")

    # Check for internal updates
    if is_new_version_available():
        should_update = input("New internal updates are available. Do you want to update now? (Y/N): ").lower()
        if should_update == 'y':
            display_update_log()
            input("\nPress enter to continue...")

    # Main loop
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_colored_logo()
        display_menu()

        choice = input("\nEnter your choice: ")
        if choice in ["1", "2", "3", "4"]:
            loading_animation()
            if choice == "1":
                temp_file_cleaner.clean_temp_files()
            elif choice == "2":
                memory_optimizer.optimize_memory()
            elif choice == "3":
                disk_cleaner.clean_disk()
            elif choice == "4":
                startup_optimizer.list_startup_programs()
        elif choice == "5":
            print(f"{Fore.RED}Exiting Dengdro...")
            break
        else:
            print(f"{Fore.LIGHTBLACK_EX}Invalid choice. Please select a valid option.")

        input("\nPress enter to return to the main menu...")

if __name__ == "__main__":
    main()
