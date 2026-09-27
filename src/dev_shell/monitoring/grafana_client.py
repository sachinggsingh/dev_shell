"""Grafana client for dev_shell monitoring."""

import json
import urllib.error
import urllib.request
from importlib.resources import files
from pathlib import Path


def _default_config_path() -> Path:
    """Return the bundled Grafana configuration path."""
    return Path(files("dev_shell.config").joinpath("grafana.json"))


class GrafanaClient:
    """Client used by dev_shell to query PromQL metrics through Grafana."""

    def __init__(self, config_path=None):
        self.host = "localhost"
        self.port = 3000
        self.api_key = None
        self.datasource_uid = None

        self._load_config(config_path or _default_config_path())
        self.base_url = f"http://{self.host}:{self.port}/api/ds/query"

    def _load_config(self, config_path):
        """Load Grafana connection settings from config."""
        config_path = Path(config_path)

        if not config_path.exists():
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            self.host = config.get("host", "localhost")
            self.port = config.get("port", 3000)
            self.api_key = config.get("api_key")
            self.datasource_uid = config.get("datasource_uid")

        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: failed to load Grafana config: {e}")

    def ping(self) -> bool:
        """Return True if Grafana responds to a health check."""
        url = f"http://{self.host}:{self.port}/api/health"
        request = urllib.request.Request(url, method="GET")

        if self.api_key:
            request.add_header("Authorization", f"Bearer {self.api_key}")

        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload.get("database") == "ok"
        except Exception:
            return False

    def query(self, promql_query):
        """Execute a PromQL instant query through Grafana."""
        if not self.datasource_uid:
            raise Exception("Grafana datasource UID is not configured")

        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {
                        "type": "prometheus",
                        "uid": self.datasource_uid,
                    },
                    "expr": promql_query,
                    "instant": True,
                    "format": "time_series",
                }
            ],
            "from": "now-5m",
            "to": "now",
        }

        request = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        if self.api_key:
            request.add_header("Authorization", f"Bearer {self.api_key}")

        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))

            return self._extract_value(data)

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise Exception(f"Grafana request failed ({e.code}): {body}") from e

        except urllib.error.URLError as e:
            raise Exception(f"Failed to connect to Grafana: {e}") from e

        except json.JSONDecodeError as e:
            raise Exception(f"Invalid response from Grafana: {e}") from e

    @staticmethod
    def _extract_value(data):
        """Extract the latest metric value from a Grafana query response."""
        results = data.get("results", {})
        result = results.get("A", {})

        if result.get("error"):
            raise Exception(result["error"])

        frames = result.get("frames", [])
        if not frames:
            return None

        frame = frames[0]
        values = frame.get("data", {}).get("values", [])

        if len(values) < 2:
            return None

        metric_values = values[1]
        if not metric_values:
            return None

        last_value = metric_values[-1]
        if last_value is None:
            return None

        if isinstance(last_value, str) and last_value.lower() == "nan":
            return None

        return float(last_value)
