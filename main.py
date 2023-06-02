#!/usr/bin/python3
import time
from helper import NewDirHandler, clear
# from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from anime import print_art

# Constant variables for directories. use the one according to the machine running the program
UBUNTU_WATCHING_DIR = "/run/user/1000/gvfs/afp-volume:host=GuruBibliotheca.local,user=gurubibliotheca,volume=Vault/Coastal Film Lab/SP-500ExportDir"
MAC_WATCHING_DIR = "/Volumes/Vault/Coastal Film Lab/Testing-grounds/SP500-Export-Bucket"
UBUNTU_TARGET_DIR = "/run/user/1000/gvfs/afp-volume:host=GuruBibliotheca.local,user=gurubibliotheca,volume=Vault/Coastal Film Lab/scannedimages"
MAC_TARGET_DIR = "/Volumes/Vault/Coastal Film Lab/Testing-grounds/weeklyfolders"
UBUNTU_TEMP_DIR = "/home/coastal/Pictures/sp500-temp-dir"
MAC_TEMP_DIR = "/Users/edrdmolina/Desktop/Temp-Folder"

# The initial path is the file path to where the scanner will export to
initial_path = UBUNTU_WATCHING_DIR

# Update this ONLY if the server directory changes. DO NOT INCLUDE WEEKLY FOLDER
initial_server_dir = UBUNTU_TARGET_DIR

# The temporary on machine directory
temp_directory = UBUNTU_TEMP_DIR


if __name__ == "__main__":

    # Prompts user for the week folder currently working on
    week = input("Input the weekly folder (MM-DD-YY): ")
    weekly_directory = initial_server_dir + "/" + week
    print(f"Will export files to {weekly_directory}")

    still_working = True

    while still_working:
        # prompt user for order information
        customer_initials = input("Input customer initials (JD): ").upper().strip()
        order_number = input("Input Order Number: (ABCDEF): ").upper().strip()
        roll_number = input("Input first roll number: ").strip()
        is_large_export = input("Will this be an extra large export? (Y/N): ").strip().upper()

        if is_large_export == 'Y':
            is_large_export = True
        else:
            is_large_export = False

        print("\nWatching out for new exports from scanner...")
        print("Hit 'CTRL-C' to shut down this program.")

        event_handler = NewDirHandler(
            temp_directory=temp_directory,
            target_directory=weekly_directory,
            customer_initials=customer_initials,
            order_number=order_number,
            roll_number=roll_number,
            is_large_export=is_large_export
        )

        observer = PollingObserver()
        observer.schedule(event_handler=event_handler, path=initial_path, recursive=True)
        observer.start()

        while event_handler.observe:
            # Time asleep controls how often the CPU checks for a new dir created
            # The more time spent asleep the less load on the CPU
            time.sleep(1)
                
        observer.stop()    
        observer.join()

        # Prompts user to check if there are more orders.
        continue_prompt = input("\nAre there more orders for today? (Y/N): ").upper()

        if continue_prompt == "N":
            still_working = False

            print_art()

            time.sleep(5)

        else:
            clear()
