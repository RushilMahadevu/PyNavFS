from datetime import datetime
import shutil
from pathlib import Path
from colorama import Fore, Style
import os
import subprocess
import platform
import sys
import difflib

class FileExplorer:
    def __init__(self):
        self.current_path = Path.cwd()

    def suggest_command(self, input_command):
        # Suggest similar commands for unrecognized input.
        commands = ["ls", "cd", "mkdir", "rm", "touch", "open", "run", "cat", "find", "help", "exit"]
        matches = difflib.get_close_matches(input_command, commands, n=3, cutoff=0.6)
        if matches:
            print(Fore.MAGENTA + f"Did you mean: {', '.join(matches)}?")
        else:
            print(Fore.MAGENTA + "No similar commands found.")

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


    def run_python_file(self, filename):
        # Run a Python script
        file_path = self.current_path / filename
        if not file_path.exists():
            print(Fore.RED + f"File not found: {filename}")
            return
        if not filename.endswith('.py'):
            print(Fore.RED + f"Not a Python file: {filename}")
            return

        try:
            print(Fore.CYAN + f"Running {filename}...")
            subprocess.run([sys.executable, file_path], check=True)
            print(Fore.GREEN + f"Finished running {filename}")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error running script: {e}")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
    
    def cat_file(self, filename):
        # Display the contents of a file
        file_path = self.current_path / filename
        if not file_path.exists():
            print(Fore.RED + f"File not found: {filename}")
            return
        if file_path.is_dir():
            print(Fore.RED + f"Error: {filename} is a directory")
            return

        try:
            with open(file_path, 'r') as f: # open file in read mode and assign to f
                content = f.read()
                print(Fore.CYAN + f"\nContents of {filename}:")
                print(Style.RESET_ALL + content)
        except Exception as e:
            print(Fore.RED + f"Error reading file: {e}")
    
    def find(self, name):
        # Search for files or directories by name in the current directory and its subdirectories.
        try:
            print(Fore.CYAN + f"\nSearching for '{name}' in {self.current_path}...\n")
            matches = []
            for root, dirs, files in os.walk(self.current_path):
                if name in dirs or name in files:
                    full_path = Path(root) / name
                    matches.append(full_path)

            if matches:
                print(Fore.GREEN + "Found the following matches:")
                for match in matches:
                    print(Fore.LIGHTBLUE_EX + str(match))
            else:
                print(Fore.YELLOW + f"No matches found for '{name}'.")
        except Exception as e:
            print(Fore.RED + f"Error searching for '{name}': {e}")

    def mv(self, source, destination):
        # Move or rename a file/directory
        try:
            src_path = self.current_path / source
            dst_path = self.current_path / destination
            
            if not src_path.exists():
                print(Fore.RED + f"Error: {source} not found")
                return
                
            # Determine operation type
            is_move = src_path.parent != dst_path.parent
            is_rename = src_path.name != dst_path.name
            
            src_path.rename(dst_path)
            
            # Provide appropriate feedback
            if is_move and is_rename:
                print(Fore.GREEN + f"Moved and renamed: {source} -> {destination}")
            elif is_move:
                print(Fore.GREEN + f"Moved: {source} -> {destination}")
            else:
                print(Fore.GREEN + f"Renamed: {source} -> {destination}")
                
        except FileExistsError:
            print(Fore.RED + f"Error: {destination} already exists")
        except Exception as e:
            print(Fore.RED + f"Error moving/renaming: {e}")

    def copy(self, source, destination):
        # Copy a file or directory to destination
        try:
            src_path = self.current_path / source
            dst_path = self.current_path / destination
            
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
                print(Fore.GREEN + f"Copied file: {source} -> {destination}")
            elif src_path.is_dir():
                shutil.copytree(src_path, dst_path)
                print(Fore.GREEN + f"Copied directory: {source} -> {destination}")
            else:
                print(Fore.RED + f"Error: {source} not found")
                
        except FileExistsError:
            print(Fore.RED + f"Error: {destination} already exists")
        except Exception as e:
            print(Fore.RED + f"Error copying: {e}")

    def grep(self, pattern):
        # Search for a pattern in files within the current directory and subdirectories.
        try:
            print(Fore.CYAN + f"\nSearching for pattern '{pattern}' in {self.current_path}...\n")
            matches = []
            for root, _, files in os.walk(self.current_path):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            for line_number, line in enumerate(f, start=1):
                                if pattern in line:
                                    matches.append((file_path, line_number, line.strip()))
                    except UnicodeDecodeError:
                        continue  # Silently skip files that cannot be decoded as UTF-8
                    except Exception as e:
                        print(Fore.RED + f"Error reading file {file_path}: {e}")

            if matches:
                print(Fore.GREEN + "Found the following matches:")
                for match in matches:
                    print(f"{match[0]}:{match[1]}: {match[2]}")
            else:
                print(Fore.YELLOW + f"No matches found for pattern '{pattern}'.")
        except Exception as e:
            print(Fore.RED + f"Error searching for pattern '{pattern}': {e}")

        
    def print_help(self):
        print(Fore.CYAN + "\nAvailable commands:\n")
        print(Fore.GREEN + "ls                  - List contents of current directory")
        print(Fore.GREEN + "cd <path>           - Change directory")
        print(Fore.GREEN + "mkdir <name>        - Create a new directory")
        print(Fore.GREEN + "rm <name>           - Delete a file or directory")
        print(Fore.GREEN + "touch <filename>    - Create a new empty file")
        print(Fore.GREEN + "open <filename>     - Open a file with default editor")
        print(Fore.GREEN + "run <filename>      - Run a Python script")
        print(Fore.GREEN + "cat <filename>      - Display file contents")
        print(Fore.GREEN + "find <filename>     - Find a file in the current directory and subdirectories")
        print(Fore.GREEN + "mv <source> <dest>  - Move or rename files/directories (use one argument to rename)")
        print(Fore.GREEN + "cp <src> <dst>      - Copy file or directory")
        print(Fore.GREEN + "grep <pattern>      - Search for a pattern in files")
        print(Fore.GREEN + "help                - Show this help message")
        print(Fore.GREEN + "exit                - Exit the program")

