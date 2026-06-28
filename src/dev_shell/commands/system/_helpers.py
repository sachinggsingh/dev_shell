"""Shared helpers for system commands."""

import platform
import subprocess


def bytes_to_human(num_bytes: float) -> str:
    """Convert bytes to a human-readable string (e.g. '1.23 GB')."""
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} PB"


def section(title: str) -> None:
    """Print a formatted section header."""
    width = 44
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def row(label: str, value: str, indent: int = 2) -> None:
    """Print a single label/value row."""
    pad = " " * indent
    print(f"{pad}{label:<22}{value}")


def run(cmd: list, timeout: int = 10) -> str:
    """Run a subprocess command and return stdout."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def current_os() -> str:
    """Return a normalised OS identifier: 'linux', 'darwin', or 'windows'."""
    return platform.system().lower()
