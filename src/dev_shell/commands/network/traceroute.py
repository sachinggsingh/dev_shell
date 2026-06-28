"""Traceroute command."""

import platform
import subprocess


def traceroute(args):
    if not args:
        print("Usage: traceroute <hostname> [-d]")
        return

    target = None
    flags = []
    for arg in args:
        if arg.startswith("-"):
            flags.append(arg)
        elif target is None:
            target = arg

    if not target:
        print("Usage: traceroute <hostname> [-d]")
        return

    try:
        if platform.system().lower() == "windows":
            command = ["tracert"] + flags + [target]
        else:
            if "-d" in flags:
                flags.remove("-d")
                flags.append("-n")
            command = ["traceroute"] + flags + [target]

        print(f"Tracing the path to {target}... Please wait.\n")

        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ) as process:
            for line in process.stdout:
                print(line, end="", flush=True)
            process.wait()

    except Exception as e:
        print(f"Error: {e}")
