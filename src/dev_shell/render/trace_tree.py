"""Renders a single trace's span tree (used by `trace <trace_id>`)."""


def _build_tree(spans: list) -> dict:
    """Turn Jaeger's flat span list into a parent_id -> [children] map,
    plus a lookup of span_id -> span, and find the root span(s)."""
    by_id = {span["span_id"]: span for span in spans}
    children = {}
    roots = []

    for span in spans:
        parent_id = span.get("parent_id")
        if parent_id and parent_id in by_id:
            children.setdefault(parent_id, []).append(span)
        else:
            roots.append(span)

    return {"by_id": by_id, "children": children, "roots": roots}


def _duration_bar(duration_ms: int, max_ms: int, width: int = 30) -> str:
    if max_ms <= 0:
        return ""
    filled = max(1, round((duration_ms / max_ms) * width))
    return "█" * filled


def _render_span(span, children_map, max_ms, depth=0, lines=None):
    if lines is None:
        lines = []

    indent = "  " * depth
    duration = span.get("duration_ms", 0)
    bar = _duration_bar(duration, max_ms)
    error_flag = " [ERROR]" if span.get("error") else ""
    lines.append(f"{indent}{span.get('operation', '?')} ({duration}ms){error_flag}")
    if bar:
        lines.append(f"{indent}{bar}")

    for log in span.get("logs", []):
        msg = log.get("message") or log
        lines.append(f"{indent}  · {msg}")

    for child in children_map.get(span["span_id"], []):
        _render_span(child, children_map, max_ms, depth + 1, lines)

    return lines


def render_trace_tree(trace: dict):
    """
    trace: dict shaped like:
        {"trace_id": str, "spans": [
            {"span_id": str, "parent_id": str|None, "operation": str,
             "duration_ms": int, "tags": {...}, "logs": [...], "error": bool}
        ]}
    """
    spans = trace.get("spans", [])
    trace_id = trace.get("trace_id", "?")

    print(f"Trace {trace_id}")
    print("-" * max(len(f"Trace {trace_id}"), 40))

    if not spans:
        print("  (no spans found)")
        return

    tree = _build_tree(spans)
    max_ms = max((s.get("duration_ms", 0) for s in spans), default=0)

    lines = []
    for root in tree["roots"]:
        _render_span(root, tree["children"], max_ms, depth=0, lines=lines)

    print("\n".join(lines))
    print()
    error_count = sum(1 for s in spans if s.get("error"))
    print(f"  {len(spans)} span(s), {error_count} error(s).")