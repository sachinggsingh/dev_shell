"""File manipulation commands."""

from . import inspect, listing, read, remove, search, transfer, write


class FileCommands:
    """Handles file-related shell commands."""

    ls = staticmethod(listing.ls)
    cat = staticmethod(read.cat)
    head = staticmethod(read.head)
    tail = staticmethod(read.tail)
    touch = staticmethod(write.touch)
    edit = staticmethod(write.edit)
    rm = staticmethod(remove.rm)
    find = staticmethod(search.find)
    grep = staticmethod(search.grep)
    move = staticmethod(transfer.move)
    cp = staticmethod(transfer.cp)
    rename = staticmethod(transfer.rename)
    file_size = staticmethod(inspect.file_size)
    stat = staticmethod(inspect.stat)
    checksum = staticmethod(inspect.checksum)
    diff = staticmethod(inspect.diff)
