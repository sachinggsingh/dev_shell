"""Directory manipulation commands."""

from . import create, navigation, tree


class DirectoryCommands:
    """Handles directory-related dev_shell commands."""

    pwd = staticmethod(navigation.pwd)
    cd = staticmethod(navigation.cd)
    mkdir = staticmethod(create.mkdir)
    rmdir = staticmethod(create.rmdir)
    tree = staticmethod(tree.tree)
