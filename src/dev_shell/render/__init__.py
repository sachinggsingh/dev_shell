"""Terminal rendering layer for dev_shell monitoring.

Every module here is pure presentation: functions take plain dicts/lists
(already fetched by monitoring/providers/*) and write formatted output to
the terminal. Nothing in this package performs I/O against Prometheus,
Jaeger, or Grafana — that boundary is what lets watch/traces/trace reuse
the same renderers regardless of which backend supplied the data.
"""

from .metrics_panel import render_metrics_panel
from .trace_table import render_traces_table
from .trace_tree import render_trace_tree

__all__ = ["render_metrics_panel", "render_trace_tree", "render_traces_table"]
