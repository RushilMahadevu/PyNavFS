# 🗂️ PyNavFS

A lightweight, terminal-based file system navigator and explorer written in Python. PyNavFS provides an intuitive command-line interface for basic file system operations including browsing, creating, copying, moving, and managing files and folders.

## ✨ Features
- 📁 Directory navigation
- 📋 File and directory listing with details (size, modification time)
- ➕ Create and delete files/directories
- 🔄 Move and copy files/directories
- 🔍 Open files with system default applications
- 🎨 Color-coded interface for better visibility
- 🐍 Run Python scripts directly
- 📝 View file contents (cat command)
- 🔍 Search for files and directories by name (find command)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/RushilMahadevu/PyNavFS.git
```

2. Navigate to the project directory:
```bash
cd PyNavFS
```


## 💻 Usage

Run the program:
```bash
python main.py
```

### Available Commands:
- `ls` - List contents of current directory
- `cd <path>` - Change directory
- `mkdir <name>` - Create a new directory
- `rm <name>` - Delete a file or directory
- `touch <filename>` - Create a new empty file
- `open <filename>` - Open a file with system default editor
- `run <filename>` - Run a Python script
- `cat <filename>` - Display file contents
- `find <name>` - Search for files or directories by name
- `mv <source> <destination>` - Move or rename files/directories
- `cp <source> <destination>` - Copy files or directories
- `help` - Show help message
- `exit` - Exit the program

### Examples:
```bash
# Copy a file
cp document.txt backup.txt

# Move a file to another directory
mv document.txt documents/

# Rename a file
mv oldname.txt newname.txt
```

## 🔧 Requirements
- Python 3.x
- colorama >= 0.4.6

## 📝 License
MIT License

