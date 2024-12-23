# 🗂️ PyNavFS

A lightweight, terminal-based file system navigator and explorer written in Python. PyNavFS provides an intuitive command-line interface for basic file system operations like browsing directories, creating/deleting files and folders, and opening files.

## ✨ Features
- 📁 Directory navigation
- 📋 File and directory listing with details (size, modification time)
- ➕ Create and delete files/directories
- 🔍 Open files with system default applications
- 🎨 Color-coded interface for better visibility
- 🐍 Run Python scripts directly
- 📝 View file contents (cat command)

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
- `help` - Show help message
- `exit` - Exit the program

## 🔧 Requirements
- Python 3.x
- colorama >= 0.4.6

## 📝 License
MIT License