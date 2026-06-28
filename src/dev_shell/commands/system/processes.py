"""Process listing commands."""

import time

import psutil

from ._helpers import section


def processes(args):
    """Display running processes sorted by CPU usage.

    Usage:
      processes           Show top 10 processes
      processes -n 20     Show top N processes
      processes -a        Show all processes
    """
    try:
        show_all = "-a" in args
        limit = None

        if not show_all:
            limit = 10
            if "-n" in args:
                idx = args.index("-n")
                if idx + 1 < len(args):
                    try:
                        limit = int(args[idx + 1])
                    except ValueError:
                        print("[processes] Invalid value for -n; using default 10.")

        proc_list = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                proc_list.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        time.sleep(0.2)
        proc_list.clear()
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                proc_list.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        proc_list.sort(key=lambda p: p.get("cpu_percent") or 0.0, reverse=True)

        if not show_all and limit:
            proc_list = proc_list[:limit]

        label = "All" if show_all else f"Top {limit}"
        section(f"Processes ({label})")
        print(f"  {'PID':>7}  {'Name':<30} {'CPU%':>6}  {'MEM%':>6}")
        print("  " + "-" * 55)
        for p in proc_list:
            pid = p.get("pid", "?")
            name = (p.get("name") or "")[:29]
            cpu = p.get("cpu_percent") or 0.0
            mem = p.get("memory_percent") or 0.0
            print(f"  {pid:>7}  {name:<30} {cpu:>5.1f}%  {mem:>5.1f}%")

    except Exception as exc:
        print(f"[processes] Error: {exc}")
