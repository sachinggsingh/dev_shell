# dev_shell

A custom developer shell built in Python for file and system operations, designed to be modular, extensible, and easy to extend with new commands.

## About

`dev_shell` is a lightweight shell environment that mimics basic command line behavior with project-specific utilities and structured command modules.
It is built for developers who want an extensible local shell experience with custom commands like `watch`, `perm`, `tree`, and more.

## Project Structure

```
dev_shell/
├── main.py                 # Shell entry point
├── shell.py                # Core shell dispatcher and command registry
├── commands/               # Command modules grouped by feature
│   ├── __init__.py
│   ├── file_commands.py    # File-related commands (touch, rm, ls, cat, size)
│   ├── directory_commands.py # Directory commands (pwd, cd, mkdir, rmdir, tree)
│   ├── system_commands.py  # System commands (clear, watch)
│   ├── log_commands.py     # Log viewing commands
│   ├── permission_commands.py # File permission info (perm)
│   └── help_command.py     # Help command
└── utils/                  # Shared helpers for logging, validation, formatting
    ├── __init__.py
    ├── formatters.py
    ├── logger.py
    └── validators.py
```

## Features

- Modular command registration system
- Built-in command help and dispatch
- File operations with validation and formatted output
- Directory tree browsing with filters
- Local CPU monitoring via `watch`
- File permission inspection via `perm`
- Easy to extend with new command modules

## Commands

| Command | Description | Status |
|---|---|---|
| `pwd` | Show current working directory | Done |
| `ls [path] [-a] [-l] [-d]` | List files and folders with optional hidden/long/directory-only flags | Done |
| `cd <path>` | Change current directory | Done |
| `mkdir <name> [-p]` | Create directory with optional parent creation | Done |
| `rmdir <name> [-r]` | Remove directory, optionally recursively | Done |
| `touch <name>` | Create a file if it does not exist | Done |
| `rm <name> [-f]` | Remove a file with optional force | Done |
| `tree [path] [-d]` | Display directory tree, optionally directories only | Done |
| `size <path>` | Show file size | Done |
| `perm <path>` | Show file permission flags | Done |
| `logs <file>` | Print file contents | Done |
| `watch [server-name]` | Show local CPU usage, remote support planned | Done |
| `clear` | Clear the screen | Done |
| `help` | Display help text | Done |
| `exit` / `q` | Exit the shell | Done |

## Usage

Run the shell from the `dev_shell` directory:

```bash
python main.py
```

Then type commands like:

```bash
help
ls -l
tree .
perm /path/to/file
watch local
size README.md
rm temp.txt
```

## Installation

This project uses standard Python libraries. For CPU monitoring, install `psutil`:

```bash
pip install -r requirements.txt
```

## Extending `dev_shell`

### Add a new command

1. Create a module under `commands/`, for example `commands/search_commands.py`.
2. Implement a command class and static handler:

```python
class SearchCommands:
    @staticmethod
    def grep(args):
        """Search for text in files."""
        # implementation here
        pass
```

3. Import and register the command in `shell.py`:

```python
from commands.search_commands import SearchCommands

self.commands = {
    # ... existing commands
    "grep": SearchCommands.grep,
}
```

4. Add help text to `commands/help_command.py`.

## Notes

- `watch <server-name>` currently supports local monitoring. Remote monitoring via SSH or an agent is planned.
- The `utils/` package provides reusable formatting, logging, and validation helpers for command modules.
- This project is designed to be easy to scale with new commands and shell behaviors.

## Next Improvements

- Add remote `watch` via SSH or monitoring agent
- Add `stats` command for system and repository metrics
- Add `dashboard` command for summary output
- Add aliases and configuration support
