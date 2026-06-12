# dev_shell

A custom developer shell built in Python for file and system operations, designed to be modular, extensible, and easy to extend with new commands.

## About

`dev_shell` is a lightweight shell environment that mimics basic command line behavior with project-specific utilities and structured command modules.

It is built for developers who want an extensible local shell experience with custom commands like `watch`, `perm`, `tree`, and more.

Beyond basic shell functionality, dev_shell is evolving toward a lightweight observability and monitoring platform capable of monitoring local systems, remote servers, and eventually Kubernetes workloads.

---

## Features

### Modular Command System

Commands are organized into self-contained modules grouped by feature area (file operations, directory operations, system monitoring, etc.). New commands can be added by creating a module and registering it with the shell dispatcher — no changes to the core shell logic are required.

### Shell Experience

dev_shell provides a familiar interactive shell experience with command history, line editing, and tab completion powered by `readline` on Linux and macOS. It supports a prompt-based workflow similar to traditional Unix shells.

### File Operations

A full set of file management commands including creating, removing, finding, and inspecting files. All operations include input validation and produce cleanly formatted output, making it easy to work with files directly from within the shell.

### Directory Browsing

The `tree` command lets you visualize directory structures with options to filter by directories only, show full paths, and limit traversal depth — useful for quickly understanding project layouts.

### File Permission Inspection

The `perm` command displays detailed file permission flags (read, write, execute) for the owner, group, and others, giving you quick visibility into access control without leaving the shell.

### Log Viewing

The `logs` command prints file contents directly in the shell, providing a quick way to inspect log files or any text file without switching to another tool.

### Local System Monitoring

dev_shell can monitor the local machine's CPU usage (overall and per-core) and memory usage in real time. This is powered by `psutil` and provides a live, updating view of system resource consumption.

### Server Registration and Management

You can register remote servers by name, IP, and port, then list or remove them. A default `local` server is always available. This forms the foundation for multi-server monitoring workflows.

### Real-Time Metric Watching

The `watch` command connects to a registered server and streams live metrics (CPU, memory) at a configurable interval. You can specify which metrics to display and how many samples to collect, making it a flexible tool for both quick checks and longer monitoring sessions.

---

## Commands

| Command                                                       | Description                                                           |
| ------------------------------------------------------------- | --------------------------------------------------------------------- |
| `pwd`                                                         | Show current working directory                                        |
| `ls [path] [-a] [-l] [-h] [-d]`                               | List files and folders with optional hidden/long/human-readable/dir flags |
| `cd <path>`                                                   | Change current directory                                              |
| `mkdir <name> [-p]`                                           | Create directory with optional parent creation                        |
| `rmdir <name> [-r]`                                           | Remove directory, optionally recursively                              |
| `touch <name>`                                                | Create a file if it does not exist                                    |
| `rm <name> [-f]`                                              | Remove a file with optional force                                     |
| `find <name> [-f] [-d] [-l]`                                  | Find files or directories recursively                                 |
| `tree [path] [-d] [-f] [-L depth]`                            | Display directory tree with filters and depth control                 |
| `size <path>`                                                 | Show file or directory size                                           |
| `perm <path>`                                                 | Show file permission flags                                            |
| `logs <file>`                                                 | Print file contents                                                   |
| `watch <server-name> [-i seconds] [-m cpu,memory] [-n count]` | Watch server metrics in real time                                     |
| `watch-server <server-name>`                                  | Explicit server monitoring command                                    |
| `add-server <name> <ip> <port>`                               | Register a server for monitoring                                      |
| `remove-server <name>`                                        | Remove a registered server                                            |
| `servers`                                                     | List all registered servers                                           |
| `ping <host>`                                                 | Send ICMP ECHO_REQUEST to network hosts                               |
| `dns <hostname>`                                              | Resolve a hostname to an IP address                                   |
| `ip [options] [target]`                                       | Show IP addresses for a host (IPv4/IPv6)                              |
| `curl <url> [-X method] [-H header] [-d data]`                | Make HTTP requests to a URL                                           |
| `traceroute <hostname> [-d]`                                  | Print the route packets trace to network host                         |
| `nslookup <hostname>`                                         | Query Internet name servers interactively                             |
| `clear`                                                       | Clear the screen                                                      |
| `help`                                                        | Display help text                                                     |
| `exit` / `q`                                                  | Exit the shell                                                        |

---

## Getting Started

Run the shell:

```bash
python main.py
```

### Optional Dependency

```bash
pip install psutil
```

Required for CPU and memory monitoring features.

---

## Watch Command — Usage Examples

The `watch` command is used to monitor server metrics in real time.

### Watch Local Machine

Monitor the local machine with default settings:

```bash
dev_shell> watch local
```

### Set a Custom Refresh Interval

Update metrics every 3 seconds:

```bash
dev_shell> watch local -i 3
```

### Choose Specific Metrics

Monitor only CPU usage:

```bash
dev_shell> watch local -m cpu
```

Monitor both CPU and memory:

```bash
dev_shell> watch local -m cpu,memory
```

### Limit the Number of Samples

Collect 10 metric snapshots and then stop:

```bash
dev_shell> watch local -n 10
```

### Combine All Options

Watch the `web1` server, refreshing every 5 seconds, showing CPU and memory, for 20 samples:

```bash
dev_shell> watch web1 -i 5 -m cpu,memory -n 20
```

### Watch a Registered Remote Server

After registering a server with `add-server`, you can watch it the same way:

```bash
dev_shell> add-server web1 192.168.1.20 9000
Server 'web1' registered at 192.168.1.20:9000

dev_shell> watch web1
```

> **Note:** Remote servers must expose a `GET /metrics` endpoint returning JSON with `cpu` and `memory` fields. Server registrations are stored in memory and will be lost when the `dev_shell` exits. A `local` server at `127.0.0.1:8000` is always registered by default.

---

## Architecture

### Project Structure

```text
dev_shell/
├── main.py                 # Shell entry point
├── shell.py                # Core shell dispatcher and command registry
├── requirements.txt        # Python dependencies
├── commands/               # Command modules grouped by feature
│   ├── directory_commands.py
│   ├── file_commands.py
│   ├── help_command.py
│   ├── log_commands.py
│   ├── network_commands.py
│   ├── permission_commands.py
│   ├── server_commands.py
│   ├── system_commands.py
│   ├── tree_command.py
│   └── watch_command.py
│
├── config/                 # Configuration files
│   └── prometheus.json
│
├── monitoring/             # Monitoring and observability clients
│   ├── prometheus_client.py
│   └── queries.py
│
├── tests/                  # Unit tests
│   └── test_network_commands.py
│
└── utils/                  # Shared utilities
    ├── formatters.py
    ├── logger.py
    └── validators.py
```

### Current Monitoring Architecture

dev_shell currently supports monitoring the local machine directly via `psutil`.

```text
dev_shell
    |
    v
Local Machine Metrics (CPU, Memory)
```

For remote servers, `dev_shell` makes HTTP requests to a `/metrics` endpoint exposed by the target server.

```text
dev_shell ──── HTTP GET /metrics ────> Remote Server
    |
    v
Display Metrics in Shell
```

### Planned Architecture — Agent-Based Registration

The next evolution replaces manual server registration with self-registering monitoring agents.

Each monitored machine will run a lightweight agent that automatically registers itself with `dev_shell`, sends periodic heartbeats, and exposes a metrics endpoint.

```text
+-------------------+
|     dev_shell      |
| Monitoring Server |
+---------+---------+
          ^
          |
      Registration
      + Heartbeat
          |
+---------+---------+
| Monitoring Agent  |  (runs on each target machine)
+-------------------+
```

**Registration Flow:**

1. Monitoring agent starts on the target machine.
2. Agent sends a registration request to `dev_shell`.
3. `dev_shell` stores the server in its registry.
4. Agent sends periodic heartbeats to confirm availability.
5. User monitors the server via `watch`.

---

## Working on Commands

The following command categories are currently in development or planned for future releases:

### File Management
* Advanced file operations
* Batch file operations
* File search and filtering

### File Editing
* In-dev_shell text editor integration
* Quick file editing commands

### System Information
* Detailed system information display
* Hardware specifications
* OS and environment details

### Process Management
* Process listing and monitoring
* Process control commands
* Resource usage per process

### Networking
* Network status commands
* Connection monitoring
* DNS resolution tools
* Network diagnostics

### Git Commands
* Git integration within the shell
* Repository status and operations
* Commit and branch management

### Docker Commands
* Docker container management
* Image operations
* Container monitoring and logs

### Kubernetes Commands
* Kubernetes cluster interaction
* Pod and deployment management
* Resource monitoring

### Server Monitoring
* Enhanced server health checks
* Performance metrics aggregation
* Multi-server dashboards

---

## Future Scope

### Agent-Based Remote Monitoring

* Self-registering servers via lightweight agents
* Heartbeat system for online/offline detection
* Remote CPU and memory monitoring
* Automatic server registry management

### Kubernetes Service Discovery

In Kubernetes environments, pods are ephemeral — they are created and destroyed dynamically, and their IP addresses change constantly. Manual server registration becomes impractical at scale.

`dev_shell` will integrate with the Kubernetes API to automatically discover running workloads and register them as monitoring targets.

```text
Kubernetes Cluster
        |
        v
Kubernetes API Server
        |
        v
dev_shell Discovery Engine
        |
        +---- Pod A
        +---- Pod B
        +---- Pod C
```

**Planned capabilities:**

* Automatic discovery of pods, deployments, and services
* Dynamic target registration as workloads scale up or down
* Kubernetes-native monitoring without manual configuration
* Foundation for a broader observability platform

### dev_shell Enhancements

* Command aliases
* Configuration file support
* Improved tab completion
* Better output formatting

### Observability with Prometheus

`dev_shell` now natively integrates with Prometheus to provide advanced real-time observability for registered servers.

**Prometheus Integration Features:**
* **Prometheus Client**: Connects to a Prometheus instance (defaulting to `localhost:9090`, configurable via `config/prometheus.json`).
* **Rich Metrics**: The `watch` and `watch-server` commands have been upgraded to execute PromQL queries and render a live dashboard directly in the terminal.
* **Tracked Telemetry**: `dev_shell` tracks CPU usage, memory consumption, requests per second, error rate, and P95 latency for each server based on its associated Prometheus `job`.

**Future Observability Goals:**
* Dashboard command for a consolidated metrics overview
* Stats command for aggregated metric summaries
* Alerting support for threshold-based notifications
* Log aggregation across monitored servers

---

## Goals

The long-term goal of `dev_shell` is to evolve from a custom developer shell into a lightweight observability and monitoring platform while remaining easy to understand, extend, and experiment with.
