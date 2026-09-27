"""Process Commands."""

from .ps import ps


class Processes:
    """Handles processes-related shell commands."""

    execute = staticmethod(ps)
