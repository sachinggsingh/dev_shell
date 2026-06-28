"""Log viewing commands."""

from .logs import logs


class LogCommands:
    """Handles log-related shell commands."""

    logs = staticmethod(logs)
