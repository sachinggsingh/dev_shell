"""Renders a live-refreshing metrics summary panel (used by `watch`)."""

import shutil

CLEAR_AND_HOME = "\033[2J\033[H"

# Display order + labels for known metric keys. Anything in the summary
# dict not listed here still renders, just appended after these in
# whatever order the dict provides.
KNOWN_METRICS = [
    ("cpu", "CPU", "%"),
    ("memory", "Memory", "bytes"),
    ("requests_per_sec", "Requests/sec", "req/s"),
    ("error_rate", "Error rate", "err/s"),
    ("latency_p95", "P95 latency", "s"),
]


def _format_value(value, unit):
    if value is None:
        return "n/a"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)

    if unit == "bytes":
        for scale, suffix in [(1024**3, "GB"), (1024**2, "MB"), (1024, "KB")]:
            if value >= scale:
                return f"{value / scale:.2f} {suffix}"
        return f"{value:.0f} B"
    if unit == "%":
        return f"{value:.1f}%"
    return f"{value:.3f} {unit}".rstrip()


def render_metrics_panel(summary: dict, source_name: str = "", target: str = "", clear: bool = True):
    """Draw one refresh frame of the metrics panel.

    summary: dict of metric_name -> raw value, as returned by
             Provider.get_summary(). Missing keys are simply skipped.
    source_name: label for which connected source this came from (e.g. "prometheus-main")
    target: label for what's being watched (e.g. a job name or service name)
    clear: if True, clears the terminal before drawing (set False for testing/logging)
    """
    width = shutil.get_terminal_size(fallback=(80, 24)).columns
    lines = []

    header = f" dev_shell watch — {source_name}"
    if target:
        header += f" / {target}"
    lines.append(header)
    lines.append("-" * min(width, max(len(header), 40)))

    seen = set()
    for key, label, unit in KNOWN_METRICS:
        if key in summary:
            lines.append(f"  {label:<15} {_format_value(summary[key], unit)}")
            seen.add(key)

    # Any extra/unknown keys in the summary still get shown, raw.
    for key, value in summary.items():
        if key not in seen:
            lines.append(f"  {key:<15} {value}")

    lines.append("")
    lines.append("  Press Ctrl+C to stop watching.")

    output = "\n".join(lines)
    if clear:
        print(CLEAR_AND_HOME + output, end="", flush=True)
    else:
        print(output)