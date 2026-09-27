"""Grafana metrics provider."""

from dev_shell.monitoring.grafana_client import GrafanaClient
from dev_shell.monitoring.queries import Queries

from .base import Provider


class GrafanaProvider(Provider):
    """Fetch PromQL metrics through Grafana's datasource query API."""

    kind = "grafana"

    def __init__(self, client: GrafanaClient | None = None):
        self.client = client or GrafanaClient()

    def ping(self) -> bool:
        return self.client.ping()

    def get_summary(self, job_name: str) -> dict:
        """Return headline metrics for a Prometheus job via Grafana."""
        queries = Queries.get_queries(job_name)
        summary = {}

        for name, promql in queries.items():
            value = self.client.query(promql)
            summary[name] = self._normalize(name, value)

        return summary

    @staticmethod
    def _normalize(metric_name: str, value):
        """Convert raw PromQL results into values the render layer expects."""
        if value is None:
            return None

        if metric_name == "cpu":
            return float(value) * 100

        return float(value)
