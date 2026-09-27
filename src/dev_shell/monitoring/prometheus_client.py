"""Prometheus client for dev_shell monitoring."""

import json
import urllib.error
import urllib.parse
import urllib.request
from importlib.resources import files
from pathlib import Path


def _default_config_path() -> Path:
    """Return the default Prometheus configuration path."""
    return Path(
        files("dev_shell.config").joinpath("prometheus.json")
    )


class PrometheusClient:
    """Client for querying Prometheus metrics."""

    def __init__(self, config_path=None):
        self.host = "localhost"
        self.port = 9090

        self._load_config(
            config_path or _default_config_path()
        )

        # Prometheus instant query API.
        self.base_url = (
            f"http://{self.host}:{self.port}/api/v1/query"
        )

    def _load_config(self, config_path):
        """Load Prometheus configuration from a JSON file."""
        config_path = Path(config_path)

        if not config_path.exists():
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            self.host = config.get("host", "localhost")
            self.port = config.get("port", 9090)

        except (json.JSONDecodeError, OSError) as e:
            print(
                f"Warning: Failed to load Prometheus config: {e}"
            )

    def query(self, promql_query):
        """Execute a PromQL instant query and return the value."""
        params = urllib.parse.urlencode({
            "query": promql_query,
        })

        url = f"{self.base_url}?{params}"

        try:
            with urllib.request.urlopen(
                url,
                timeout=5,
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            if data.get("status") != "success":
                error = data.get(
                    "error",
                    "Unknown Prometheus error",
                )

                raise Exception(
                    f"Prometheus query failed: {error}"
                )

            result = data.get(
                "data",
                {},
            ).get("result", [])

            if not result:
                return None

            value = result[0].get("value")

            if not value or len(value) < 2:
                return None

            return float(value[1])

        except urllib.error.URLError as e:
            raise Exception(
                f"Failed to connect to Prometheus: {e}"
            ) from e

        except json.JSONDecodeError as e:
            raise Exception(
                f"Invalid response from Prometheus: {e}"
            ) from e

        except Exception as e:
            raise Exception(
                f"Query failed: {e}"
            ) from e