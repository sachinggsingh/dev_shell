"""Jaeger client for dev_shell monitoring."""

import json
import urllib.error
import urllib.parse
import urllib.request
from importlib.resources import files
from pathlib import Path


def _default_config_path() -> Path:
    """Return the default Jaeger configuration path."""
    return Path(
        files("dev_shell.config").joinpath("jaeger.json")
    )


class JaegerClient:
    """Client for querying traces from Jaeger."""

    def __init__(self, config_path=None):
        self.host = "localhost"
        self.port = 16686

        self._load_config(
            config_path or _default_config_path()
        )

        # Jaeger Query HTTP API.
        self.base_url = (
            f"http://{self.host}:{self.port}"
        )

    def _load_config(self, config_path):
        """Load Jaeger configuration from a JSON file."""
        config_path = Path(config_path)

        if not config_path.exists():
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            self.host = config.get("host", "localhost")
            self.port = config.get("port", 16686)

        except (json.JSONDecodeError, OSError) as e:
            print(
                f"Warning: Failed to load Jaeger config: {e}"
            )

    def get_services(self):
        """Return services known to Jaeger."""
        url = f"{self.base_url}/api/services"

        try:
            with urllib.request.urlopen(
                url,
                timeout=5,
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            return data.get("data", [])

        except urllib.error.URLError as e:
            raise Exception(
                f"Failed to connect to Jaeger: {e}"
            ) from e

        except json.JSONDecodeError as e:
            raise Exception(
                f"Invalid response from Jaeger: {e}"
            ) from e

    def get_traces(
        self,
        service,
        limit=20,
        lookback="1h",
    ):
        """Return traces for a service."""

        params = urllib.parse.urlencode({
            "service": service,
            "limit": limit,
            "lookback": lookback,
        })

        url = f"{self.base_url}/api/traces?{params}"

        try:
            with urllib.request.urlopen(
                url,
                timeout=5,
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            return data.get("data", [])

        except urllib.error.URLError as e:
            raise Exception(
                f"Failed to connect to Jaeger: {e}"
            ) from e

        except json.JSONDecodeError as e:
            raise Exception(
                f"Invalid response from Jaeger: {e}"
            ) from e

    def get_trace(self, trace_id):
        """Return a single trace by trace ID."""
        url = f"{self.base_url}/api/traces/{trace_id}"

        try:
            with urllib.request.urlopen(
                url,
                timeout=5,
            ) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            traces = data.get("data", [])

            if not traces:
                return None

            return traces[0]

        except urllib.error.URLError as e:
            raise Exception(
                f"Failed to connect to Jaeger: {e}"
            ) from e

        except json.JSONDecodeError as e:
            raise Exception(
                f"Invalid response from Jaeger: {e}"
            ) from e