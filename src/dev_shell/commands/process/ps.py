"""Show running processes."""

import psutil


def ps(args):
    """
    List running processes.

    Usage:
        ps
        ps -cpu
        ps -mem
        ps -n <count>
        ps -pid <pid>
    """

    sort_by = None
    limit = None
    pid = None

    i = 0

    while i < len(args):
        arg = args[i]

        if arg == "-cpu":
            sort_by = "cpu"

        elif arg == "-mem":
            sort_by = "memory"

        elif arg == "-n":
            i += 1

            if i >= len(args):
                print("Error: Missing value for -n")
                return

            try:
                limit = int(args[i])
            except ValueError:
                print("Error: Invalid count")
                return

        elif arg == "-pid":
            i += 1

            if i >= len(args):
                print("Error: Missing PID")
                return

            try:
                pid = int(args[i])
            except ValueError:
                print("Error: Invalid PID")
                return

        else:
            print(f"Unknown option: {arg}")
            return

        i += 1

    processes = []

    for process in psutil.process_iter(["pid", "name", "status"]):
        try:
            info = process.info

            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"],
                    "status": info["status"],
                    "cpu": process.cpu_percent(interval=0.1),
                    "memory": process.memory_percent(),
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    if pid is not None:
        processes = [p for p in processes if p["pid"] == pid]

    if sort_by == "cpu":
        processes.sort(
            key=lambda x: x["cpu"],
            reverse=True,
        )

    elif sort_by == "memory":
        processes.sort(
            key=lambda x: x["memory"],
            reverse=True,
        )

    if limit is not None:
        processes = processes[:limit]

    print(f"{'PID':<8}{'NAME':<30}{'CPU %':<10}{'MEM %':<10}{'STATUS':<15}")

    print("-" * 75)

    for process in processes:
        print(
            f"{process['pid']:<8}"
            f"{process['name']:<30}"
            f"{process['cpu']:<10.1f}"
            f"{process['memory']:<10.1f}"
            f"{process['status']:<15}"
        )
