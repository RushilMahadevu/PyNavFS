from FileExplorer import FileExplorer
from colorama import init, Fore, Style

def main():
    init(autoreset=True)  # Initialize colorama
    explorer = FileExplorer()
    print(Fore.CYAN + "Simple File Explorer (type 'help' for commands)")

    while True:
        try:
            command = input(Fore.LIGHTYELLOW_EX + "\n> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()
            # inverse list of arguments
            args = parts[1:]

            if cmd == "ls":
                explorer.list_contents()
            elif cmd == "cd":
                if not args:
                    print(Fore.RED + "Usage: cd <path>")
                else:
                    explorer.change_directory(args[0])
            elif cmd == "mkdir":
                if not args:
                    print(Fore.RED + "Usage: mkdir <name>")
                else:
                    explorer.create_directory(args[0])
            elif cmd == "rm":
                if not args:
                    print(Fore.RED + "Usage: rm <name>")
                else:
                    explorer.delete(args[0])
            elif cmd == "help":
                explorer.print_help()
            elif cmd == "exit":
                break
            else:
                print(Fore.RED + "Unknown command. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nUse 'exit' to quit the program")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    main()