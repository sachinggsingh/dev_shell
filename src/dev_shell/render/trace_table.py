"""Renders a one-shot table of recent traces (used by `traces <service>`)."""


def _truncate(text: str, length: int) -> str:
    text = str(text)
    return text if len(text) <= length else text[: length - 1] + "…"


def render_traces_table(traces: list, service: str = ""):
    """
    traces: list of dicts shaped like:
        {"trace_id": str, "root_operation": str, "duration_ms": int,
         "span_count": int, "has_error": bool}
    """
    title = f"Recent traces" + (f" — {service}" if service else "")
    print(title)
    print("-" * max(len(title), 60))

    if not traces:
        print("  (no traces found)")
        return

    columns = [
        ("TRACE ID", 16),
        ("OPERATION", 28),
        ("DURATION", 10),
        ("SPANS", 6),
        ("ERROR", 5),
    ]
    header = "  ".join(f"{name:<{w}}" for name, w in columns)
    print(header)
    print("  ".join("-" * w for _, w in columns))

    for trace in traces:
        row = [
            _truncate(trace.get("trace_id", ""), 16),
            _truncate(trace.get("root_operation", ""), 28),
            f"{trace.get('duration_ms', 0)}ms",
            str(trace.get("span_count", 0)),
            "YES" if trace.get("has_error") else "-",
        ]
        print("  ".join(f"{val:<{w}}" for val, (_, w) in zip(row, columns)))

    print()
    print(f"  {len(traces)} trace(s). Use `trace <trace_id>` to inspect one.")