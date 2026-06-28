"""CPU monitoring commands."""

import psutil

from ._helpers import row, section


def cpu(args):
    """Display CPU information and usage.

    Usage:
      cpu           Show overall usage + cores + frequency
      cpu -p        Show per-core usage
      cpu -f        Show CPU frequency details
    """
    try:
        per_core = "-p" in args
        freq_only = "-f" in args

        section("CPU Information")

        physical = psutil.cpu_count(logical=False) or "N/A"
        logical = psutil.cpu_count(logical=True) or "N/A"
        row("Physical Cores:", str(physical))
        row("Logical Cores:", str(logical))

        if not freq_only:
            overall = psutil.cpu_percent(interval=0.5)
            row("CPU Usage:", f"{overall:.1f}%")

        if per_core:
            print()
            section("Per-Core Usage")
            per_core_pcts = psutil.cpu_percent(interval=0.5, percpu=True)
            for i, pct in enumerate(per_core_pcts):
                row(f"Core {i}:", f"{pct:.1f}%")

        print()
        section("CPU Frequency")
        freq = psutil.cpu_freq(percpu=freq_only)
        if freq is None:
            print("  Frequency data not available.")
        elif freq_only:
            for i, f in enumerate(freq):
                row(
                    f"Core {i}:",
                    f"current={f.current:.0f} MHz  "
                    f"min={f.min:.0f} MHz  max={f.max:.0f} MHz",
                )
        else:
            row("Current:", f"{freq.current:.0f} MHz")
            row("Min:", f"{freq.min:.0f} MHz")
            row("Max:", f"{freq.max:.0f} MHz")

    except Exception as exc:
        print(f"[cpu] Error: {exc}")
