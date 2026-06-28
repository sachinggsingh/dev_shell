"""Permission inspection commands."""

from .perm import perm


class Permissions:
    """Handles permission-related shell commands."""

    execute = staticmethod(perm)
