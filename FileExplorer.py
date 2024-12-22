from datetime import datetime
import shutil
from pathlib import Path
from colorama import Fore, Style
import os
import subprocess
import platform

class FileExplorer:
    def __init__(self):
        self.current_path = Path.cwd()

    def list_contents(self):
        # List all files and directories in the current path.
        print(Fore.LIGHTMAGENTA_EX + f"\nCurrent directory: {self.current_path}")
        print("-" * 80)

        # Get all entries
        entries = list(self.current_path.iterdir())

        for entry in entries:
            try:
                # Get file/directory information
                stats = entry.stat()
                modified_time = datetime.fromtimestamp(stats.st_mtime)
                entry_type = "DIR" if entry.is_dir() else "FILE"
                size = "-" if entry.is_dir() else f"{stats.st_size} bytes"

                color = Fore.LIGHTGREEN_EX if entry.is_dir() else Fore.LIGHTBLUE_EX
                print(color + f"{entry_type:<6} {entry.name:<40} {size:<15} {modified_time.strftime('%Y-%m-%d %H:%M:%S')}") 

                """
                entry_type:<6} means:
                 - take "FILE" (4 chars)
                 - left align it
                 - pad to 6 chars with spaces
                 Result: "FILE  " (4 chars + 2 spaces)

                 {name:<40} means:
                 - take "example.txt" (11 chars)
                 - left align it
                 - pad to 40 chars with spaces
                 Result: "example.txt   

                 The output would look like:
                 FILE  document.txt                             1024 bytes     2024-03-21 14:30:00
                """

            except (PermissionError, OSError) as error:
                # error accessing the file or directory
                print(Fore.RED + f"Error accessing {entry.name}: {error}")

    def change_directory(self, path):
        #Change current directory to the specified path.
        try:
            new_path = (
                self.current_path / path  # Case 1: If path != ".."
                if path != ".."          # The condition
                else self.current_path.parent  # Case 2: If path == ".."
            )

            if new_path.is_dir():  # Checks if the path is a valid directory
                self.current_path = new_path.resolve()  # Updates current path to absolute path (basically means not relative (starts from root))
                return True
            else:
                print(Fore.RED + "Error: Not a directory")  # Path exists but isn't a directory
                return False
            
        except Exception as e:
            print(Fore.RED + f"Error changing directory: {e}")
            return False

    def create_directory(self, name):
        # Create a new directory.
        try:
            new_dir = self.current_path / name  # Construct the new directory path
            new_dir.mkdir()  # Create the directory
            print(Fore.GREEN + f"Directory '{name}' created successfully")
        except FileExistsError:
            # Handle the case where the directory already exists
            print(Fore.RED + f"Error: Directory '{name}' already exists")
        except Exception as e:
            # Handle any other exceptions
            print(Fore.RED + f"Error creating directory: {e}")

    def delete(self, name):
        # Delete a file or directory.
        try:
            path = self.current_path / name  # Construct the path to the file or directory
            if path.is_dir():
                # If it's a directory, delete it and all its contents
                shutil.rmtree(path)
                print(Fore.GREEN + f"Directory '{name}' deleted successfully")
            else:
                # If it's a file, delete it
                path.unlink()
                print(Fore.GREEN + f"File '{name}' deleted successfully")
        except FileNotFoundError:
            # Handle the case where the file or directory does not exist
            print(Fore.RED + f"Error: '{name}' not found")
        except Exception as e:
            # Handle any other exceptions
            print(Fore.RED + f"Error deleting '{name}': {e}")

    def create_file(self, filename):
        """Create a new empty file"""
        file_path = self.current_path / filename
        try:
            with open(file_path, 'w') as f:
                pass  # Create empty file
            print(Fore.GREEN + f"Created file: {filename}")
        except Exception as e:
            print(Fore.RED + f"Error creating file: {e}")

    def open_file(self, filename):
        """Open a file with the default system editor"""
        file_path = self.current_path / filename
        if not file_path.exists():
            print(Fore.RED + f"File not found: {filename}")
            return

        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', file_path])
            print(Fore.GREEN + f"Opening {filename}")
        except Exception as e:
            print(Fore.RED + f"Error opening file: {e}")

    def print_help(self):
        # Display available commands.
        print(Fore.CYAN + "\nAvailable commands:\n")
        print(Fore.GREEN + "ls                  - List contents of current directory")
        print(Fore.GREEN + "cd <path>           - Change directory")
        print(Fore.GREEN + "mkdir <name>        - Create a new directory")
        print(Fore.GREEN + "rm <name>           - Delete a file or directory")
        print(Fore.GREEN + "touch <filename>    - Create a new empty file")
        print(Fore.GREEN + "open <filename>     - Open a file with default editor")
        print(Fore.GREEN + "help               - Show this help message")
        print(Fore.GREEN + "exit               - Exit the program")