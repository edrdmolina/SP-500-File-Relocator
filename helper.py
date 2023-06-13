from watchdog.events import FileSystemEventHandler
from os import name, system, chmod, listdir, path, rename
from natsort import natsorted
import shutil
import time


class NewDirHandler(FileSystemEventHandler):
    """
        This class handles what to do in the event
        where a new directory is created in the folder
    """

    def __init__(self, temp_directory, target_directory, customer_initials, order_number, roll_number, is_large_export):
        self.temp_directory = temp_directory
        self.target_directory = target_directory
        self.customer_initials = customer_initials
        self.order_number = order_number
        self.roll_number = roll_number
        self.observe = True
        self.is_large_export = is_large_export

    def on_created(self, event):
        if event.is_directory:

            old_dir = event.src_path

            roll_dir_name = f"{self.customer_initials}-{self.order_number}-{self.roll_number}"
            print(f"{roll_dir_name} Has been created")

            temp_dir = f"{self.temp_directory}/{roll_dir_name}"
            new_dir = f"{self.target_directory}/{roll_dir_name}"

            print("Found new directory, please wait while files are processed and moved to the server.")
            # Wait to allow for images to be exported in dir
            if self.is_large_export:
                time.sleep(35)
            time.sleep(10)

            move_folder(old_dir, temp_dir)
            update_file_name(temp_dir)
            move_folder(temp_dir, new_dir)
            delete_original_export(temp_dir)

            print(f"Completed export of: {roll_dir_name} >:)")
            print("On the next line hit 'Enter' for sequential roll number, different roll number, or 'N' to start a "
                  "new order")
            next_roll = input("").strip().upper()

            if next_roll == "":
                prev_roll = int(self.roll_number)
                self.roll_number = prev_roll + 1
            elif next_roll == "N":
                self.observe = False
            else:
                self.roll_number = next_roll

        
def clear():
    """
        This function clears the terminal
    """
    # for windows
    if name == 'nt':
        return system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        return system('clear')


def change_permission(target_dir, mode):
    # change permission of dir
    chmod(target_dir, mode)

    for file in listdir(target_dir):
        chmod(path.join(target_dir, file), mode)


def move_folder(old_dir, new_dir):
    try:
        shutil.move(old_dir, new_dir)
    except OSError as e:
        if e.errno == 95:
            pass
        elif e.errno == 2:
            pass
        

def delete_original_export(og_dir):
    # for file in listdir(og_dir):
    #     print(f"deleting: {path.join(og_dir, file)}")
    #     remove(path.join(og_dir, file))
    shutil.rmtree(og_dir)


def update_file_name(target_dir):
    print("Updating file names to sequential order...")
    time.sleep(3)
    counter = 1
    files = natsorted(listdir(target_dir))

    for file in files:
        extension = str(path.splitext(file)[1]).lower()
        if extension == ".jpg":
            new_name = "{:03d}.jpg".format(counter)
            rename(path.join(target_dir, file), path.join(target_dir, new_name))
            counter += 1
        elif extension == ".jpeg":
            new_name = "{:03d}.jpeg".format(counter)
            rename(path.join(target_dir, file), path.join(target_dir, new_name))
            counter += 1
        elif extension == ".tiff":
            new_name = "{:03d}.tiff".format(counter)
            rename(path.join(target_dir, file), path.join(target_dir, new_name))
            counter += 1
        elif extension == ".tif":
            new_name = "{:03d}.tif".format(counter)
            rename(path.join(target_dir, file), path.join(target_dir, new_name))
            counter += 1

