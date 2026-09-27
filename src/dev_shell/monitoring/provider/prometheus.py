# monitoring/providers/prometheus.py
from dev_shell.monitoring.prometheus_client import (
    PrometheusClient,
    PrometheusConnectionError,
    PrometheusQueryError,
    PrometheusResponseError,
)
from dev_shell.monitoring.queries import Queries

from .base import Provider


class PrometheusProvider(Provider):
    kind = "prometheus"

    def __init__(self, client: PrometheusClient = None):
        self.client = client or PrometheusClient()

    def ping(self) -> bool:
        try:
            self.client.query("up")
        except (
            PrometheusConnectionError,
            PrometheusQueryError,
            PrometheusResponseError,
        ):
            return False
        else:
            return True

    def get_summary(self, job_name: str) -> dict:
        queries = Queries.get_queries(job_name)
        return {name: self.client.query(q) for name, q in queries.items()}

    def list_jobs(self) -> list:
        return self.client.list_jobs()
