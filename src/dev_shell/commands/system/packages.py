"""Installed packages commands."""

import platform
import shutil

from ._helpers import current_os, run, section


def _packages_brew():
    if not shutil.which("brew"):
        print("  Homebrew not found.")
        return
    output = run(["brew", "list", "--versions"])
    if output:
        for line in output.splitlines():
            print(f"  {line}")
    else:
        print("  No packages found or Homebrew returned no output.")


def _packages_linux():
    if shutil.which("dpkg"):
        output = run(["dpkg", "--get-selections"])
        if output:
            print("  (apt/dpkg)")
            for line in output.splitlines():
                print(f"  {line}")
            return
    if shutil.which("dnf"):
        output = run(["dnf", "list", "installed"])
        if output:
            print("  (dnf)")
            for line in output.splitlines():
                print(f"  {line}")
            return
    if shutil.which("pacman"):
        output = run(["pacman", "-Q"])
        if output:
            print("  (pacman)")
            for line in output.splitlines():
                print(f"  {line}")
            return
    print("  No supported package manager found (apt/dnf/pacman).")


def _packages_windows():
    if not shutil.which("winget"):
        print("  winget not found.")
        return
    output = run(["winget", "list"])
    if output:
        for line in output.splitlines():
            print(f"  {line}")
    else:
        print("  No packages found or winget returned no output.")


def packages(args):
    """Display installed packages using the detected package manager.

    Usage: packages
    """
    section("Installed Packages")
    os_name = current_os()

    try:
        if os_name == "darwin":
            _packages_brew()
        elif os_name == "linux":
            _packages_linux()
        elif os_name == "windows":
            _packages_windows()
        else:
            print(f"  Unsupported OS: {platform.system()}")
    except Exception as exc:
        print(f"[packages] Error: {exc}")
