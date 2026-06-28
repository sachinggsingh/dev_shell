"""Memory monitoring commands."""

import psutil

from ._helpers import bytes_to_human, row, section


def memory(args):
    """Display memory (RAM + swap) information.

    Usage:
      memory        Show RAM usage
      memory -s     Show RAM + swap
    """
    try:
        show_swap = "-s" in args
        mem = psutil.virtual_memory()

        section("Memory Information")
        row("Total RAM:", bytes_to_human(mem.total))
        row("Used RAM:", bytes_to_human(mem.used))
        row("Free RAM:", bytes_to_human(mem.free))
        row("Available RAM:", bytes_to_human(mem.available))
        row("RAM Usage:", f"{mem.percent:.1f}%")

        if show_swap:
            print()
            section("Swap Memory")
            swap = psutil.swap_memory()
            row("Total Swap:", bytes_to_human(swap.total))
            row("Used Swap:", bytes_to_human(swap.used))
            row("Free Swap:", bytes_to_human(swap.free))
            row("Swap Usage:", f"{swap.percent:.1f}%")

    except Exception as exc:
        print(f"[memory] Error: {exc}")
