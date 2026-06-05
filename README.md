# dev_shell

A custom developer shell built in Python for file and system operations, designed to be modular, extensible, and easy to extend with new commands.

## About

`dev_shell` is a lightweight shell environment that mimics basic command line behavior with project-specific utilities and structured command modules.

It is built for developers who want an extensible local shell experience with custom commands like `watch`, `perm`, `tree`, and more.

Beyond basic shell functionality, DevShell is evolving toward a lightweight observability and monitoring platform capable of monitoring local systems, remote servers, and eventually Kubernetes workloads.

---

## Project Structure

```text
dev_shell/
├── main.py                 # Shell entry point
├── shell.py                # Core shell dispatcher and command registry
├── commands/               # Command modules grouped by feature
│   ├── __init__.py
│   ├── file_commands.py
│   ├── directory_commands.py
│   ├── system_commands.py
│   ├── log_commands.py
│   ├── permission_commands.py
│   └── help_command.py
│
├── monitoring/             # Monitoring and server discovery (future)
│   ├── registry.py
│   ├── agent.py
│   └── heartbeat.py
│
└── utils/
    ├── __init__.py
    ├── formatters.py
    ├── logger.py
    └── validators.py
```

---

## Features

* Modular command registration system
* Built-in command help and dispatch
* Command line editing, history, and tab completion using `readline` (Linux/macOS)
* File operations with validation and formatted output
* Directory tree browsing with filters
* Local CPU and memory monitoring
* File permission inspection via `perm`
* Easy to extend with new command modules
* Foundation for remote server monitoring
* Future support for automatic service discovery

---

## Commands

| Command                                                       | Description                                                           | Status |
| ------------------------------------------------------------- | --------------------------------------------------------------------- | ------ |
| `pwd`                                                         | Show current working directory                                        | Done   |
| `ls [path] [-a] [-l] [-d]`                                    | List files and folders with optional hidden/long/directory-only flags | Done   |
| `cd <path>`                                                   | Change current directory                                              | Done   |
| `mkdir <name> [-p]`                                           | Create directory with optional parent creation                        | Done   |
| `rmdir <name> [-r]`                                           | Remove directory, optionally recursively                              | Done   |
| `touch <name>`                                                | Create a file if it does not exist                                    | Done   |
| `rm <name> [-f]`                                              | Remove a file with optional force                                     | Done   |
| `tree [path] [-d] [-f] [-L depth]`                            | Display directory tree with filters and depth control                 | Done   |
| `size <path>`                                                 | Show file or directory size                                           | Done   |
| `perm <path>`                                                 | Show file permission flags                                            | Done   |
| `logs <file>`                                                 | Print file contents                                                   | Done   |
| `watch <server-name> [-i seconds] [-m cpu,memory] [-n count]` | Watch server metrics                                                  | Done   |
| `watch-server <server-name>`                                  | Explicit server monitoring command                                    | Done   |
| `add-server <name> <ip> <port>`                               | Register a server for monitoring                                      | Done   |
| `remove-server <name>`                                        | Remove a registered server                                            | Done   |
| `servers`                                                     | List all registered servers                                           | Done   |
| `clear`                                                       | Clear the screen                                                      | Done   |
| `help`                                                        | Display help text                                                     | Done   |
| `exit` / `q`                                                  | Exit the shell                                                        | Done   |

---

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

---

## Installation

This project primarily uses Python standard libraries.

Optional dependency:

```bash
pip install psutil
```

Used for:

* CPU monitoring
* Memory monitoring
* Per-core CPU statistics

---

## Monitoring Architecture

### Current Implementation

Currently DevShell supports monitoring the local machine.

```text
DevShell
    |
    v
Local Machine Metrics
```

Available metrics:

* CPU Usage
* Per-Core CPU Usage
* Memory Usage

Example:

```bash
watch local
```

---

## How to Add a Server

Use the `add-server` command to register a new server for monitoring:

```bash
add-server <name> <ip> <port>
```

### Example

```bash
shell> add-server web1 192.168.1.20 9000
Server 'web1' registered at 192.168.1.20:9000

shell> add-server db1 10.0.0.5 9000
Server 'db1' registered at 10.0.0.5:9000
```

### List Registered Servers

```bash
shell> servers
Name            IP                   Port
-------------------------------------------
local           127.0.0.1            8000
web1            192.168.1.20         9000
db1             10.0.0.5             9000
```

### Remove a Server

```bash
shell> remove-server db1
Server 'db1' removed.
```

### Monitor a Registered Server

Once added, use `watch` or `watch-server` to start monitoring:

```bash
watch web1
watch-server web1 -i 5 -m cpu,memory -n 10
```

The server must expose a `GET /metrics` endpoint returning JSON with `cpu` and `memory` fields:

```json
{
    "cpu": 42.5,
    "memory": 68.3
}
```

> **Note:** Server registrations are stored in memory and will be lost when the shell exits. A `local` server at `127.0.0.1:8000` is always registered by default.

---

## Planned Remote Monitoring (Agent-Based Registration)

The next major feature is agent-based server monitoring.

Instead of manually configuring servers, each monitored machine will run a lightweight monitoring agent.

### Architecture

```text
+-------------------+
|     DevShell      |
| Monitoring Server |
+---------+---------+
          ^
          |
      Registration
          |
+---------+---------+
| Monitoring Agent  |
+-------------------+
```

### Registration Flow

1. Monitoring agent starts.
2. Agent registers itself with DevShell.
3. DevShell stores server information.
4. User can monitor registered servers.

Example:

```bash
register web1 192.168.1.20 9000

servers

watch web1
```

### Planned Registry

```python
{
    "web1": {
        "ip": "192.168.1.20",
        "port": 9000,
        "status": "online"
    }
}
```

### Planned Agent Endpoints

```http
POST /register
POST /heartbeat
GET  /metrics
```

### Planned Features

* Self-registering servers
* Heartbeat monitoring
* Online/offline detection
* Remote CPU monitoring
* Remote memory monitoring

---

## Extending dev_shell

### Add a New Command

1. Create a module under `commands/`.

Example:

```python
class SearchCommands:

    @staticmethod
    def grep(args):
        """Search for text in files."""
        pass
```

2. Import and register the command in `shell.py`.

```python
from commands.search_commands import SearchCommands

self.commands = {
    "grep": SearchCommands.grep,
}
```

3. Add help text to `commands/help_command.py`.

---

## Future Scope: Kubernetes Service Discovery

After agent-based monitoring is implemented, DevShell will support Kubernetes-native service discovery.

### Why?

In Kubernetes environments:

* Pods are created dynamically.
* Pods can be terminated at any time.
* IP addresses change frequently.
* Manual registration becomes impractical.

Instead of registering servers manually, DevShell will automatically discover workloads using the Kubernetes API.

### Proposed Architecture

```text
Kubernetes Cluster
        |
        v
Kubernetes API Server
        |
        v
DevShell Discovery Engine
        |
        +---- Pod A
        +---- Pod B
        +---- Pod C
```

### Discovery Workflow

```text
Kubernetes API
      |
      v
Discover Pods
      |
      v
Auto Register Targets
      |
      v
Watch Metrics
```

### Planned Commands

```bash
discover k8s

pods

services

watch pod/frontend

watch deployment/api

watch service/payment
```

### Example Implementation

```python
pods = k8s.list_namespaced_pod("default")

for pod in pods.items:

    registry.register(
        pod.metadata.name,
        pod.status.pod_ip
    )
```

### Benefits

* Automatic target discovery
* No manual registration
* Kubernetes-native monitoring
* Dynamic infrastructure support
* Foundation for observability tooling

---

## Notes

* `watch local` currently supports local monitoring.
* Agent-based remote monitoring is under development.
* Kubernetes service discovery is planned for future releases.
* The `utils/` package provides reusable formatting, logging, and validation helpers.

---

## Next Improvements

### Monitoring

* Agent-based remote monitoring
* Server registry
* Heartbeat system
* Online/offline detection
* Metrics aggregation

### Shell Features

* Command aliases
* Configuration support
* Improved command completion
* Better output formatting

### Observability

* Dashboard command
* Stats command
* Alerting support
* Log aggregation
* Kubernetes service discovery

---

## Goals

The long-term goal of DevShell is to evolve from a custom developer shell into a lightweight observability and monitoring platform while remaining easy to understand, extend, and experiment with.
