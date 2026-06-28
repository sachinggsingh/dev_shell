"""System services commands."""

import platform

from ._helpers import current_os, run, section


def _services_linux():
    output = run(["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"])
    if output:
        for line in output.splitlines():
            print(f"  {line}")
    else:
        print("  Could not retrieve services. Is systemctl available?")


def _services_macos():
    output = run(["launchctl", "list"])
    if output:
        print(f"  {'PID':>7}  {'Status':>7}  Label")
        print("  " + "-" * 60)
        for line in output.splitlines()[1:]:
            parts = line.split(None, 2)
            if len(parts) == 3:
                pid, status, label = parts
                print(f"  {pid:>7}  {status:>7}  {label}")
    else:
        print("  Could not retrieve services via launchctl.")


def _services_windows():
    output = run(["sc", "query", "type=", "service", "state=", "running"])
    if output:
        for line in output.splitlines():
            print(f"  {line}")
    else:
        print("  Could not retrieve services via sc query.")


def services(args):
    """Display running system services (OS-aware).

    Usage: services
    """
    section("Running Services")
    os_name = current_os()

    try:
        if os_name == "linux":
            _services_linux()
        elif os_name == "darwin":
            _services_macos()
        elif os_name == "windows":
            _services_windows()
        else:
            print(f"  Unsupported OS: {platform.system()}")
    except Exception as exc:
        print(f"[services] Error: {exc}")
