from FileExplorer import FileExplorer
from colorama import init, Fore, Style

def main():
    init(autoreset=True)  # Initialize colorama
    explorer = FileExplorer()
    print(Style.BRIGHT + "\nSimple File Explorer (type 'help' for commands)")

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
            elif cmd == "touch":
                if not args:
                    print(Fore.RED + "Usage: touch <filename>")
                else:
                    explorer.create_file(args[0])
            elif cmd == "open":
                if not args:
                    print(Fore.RED + "Usage: open <filename>")
                else:
                    explorer.open_file(args[0])
            elif cmd == "run":
                if not args:
                    print(Fore.RED + "Usage: run <filename>")
                else:
                    explorer.run_python_file(args[0])
            elif cmd == "cat":
                if not args:
                    print(Fore.RED + "Usage: cat <filename>")
                else:
                    explorer.cat_file(args[0])
            elif cmd == "exit":
                break
            else:
                print(Fore.RED + "\nUnknown command. Type 'help' for available commands.")
                explorer.suggest_command(cmd)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nUse 'exit' to quit the program")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    main()