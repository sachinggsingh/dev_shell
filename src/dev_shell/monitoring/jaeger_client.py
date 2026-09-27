"""Jaeger client for dev_shell monitoring."""

import json
import urllib.error
import urllib.parse
import urllib.request
from importlib.resources import files
from pathlib import Path


def _default_config_path() -> Path:
    """Return the default Jaeger configuration path."""
    return Path(files("dev_shell.config").joinpath("jaeger.json"))


class JaegerConnectionError(Exception):
    """Raised when unable to connect to Jaeger."""


class JaegerResponseError(Exception):
    """Raised when Jaeger returns an invalid or unexpected response."""


class JaegerClient:
    """Client for querying traces from Jaeger."""

    def __init__(self, config_path=None):
        self.host = "localhost"
        self.port = 16686

        self._load_config(config_path or _default_config_path())

        # Jaeger Query HTTP API.
        self.base_url = f"http://{self.host}:{self.port}"

    def _load_config(self, config_path):
        """Load Jaeger configuration from a JSON file."""
        config_path = Path(config_path)

        if not config_path.exists():
            return

        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)

            self.host = config.get("host", "localhost")
            self.port = config.get("port", 16686)

        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Failed to load Jaeger config: {e}")

    def _fetch(self, url: str) -> dict:
        """Fetch and parse JSON from a Jaeger HTTP endpoint."""
        req = urllib.request.Request(url)  # noqa: S310
        try:
            with urllib.request.urlopen(req, timeout=5) as response:  # noqa: S310
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise JaegerConnectionError(  # noqa: TRY003
                f"Failed to connect to Jaeger: {e}"
            ) from e
        except json.JSONDecodeError as e:
            raise JaegerResponseError(  # noqa: TRY003
                f"Invalid response from Jaeger: {e}"
            ) from e

    def get_services(self):
        """Return services known to Jaeger."""
        url = f"{self.base_url}/api/services"
        data = self._fetch(url)
        return data.get("data", [])

    def get_traces(
        self,
        service,
        limit=20,
        lookback="1h",
    ):
        """Return traces for a service."""

        params = urllib.parse.urlencode(
            {
                "service": service,
                "limit": limit,
                "lookback": lookback,
            }
        )

        url = f"{self.base_url}/api/traces?{params}"
        data = self._fetch(url)
        return data.get("data", [])

    def get_trace(self, trace_id):
        """Return a single trace by trace ID."""
        url = f"{self.base_url}/api/traces/{trace_id}"
        data = self._fetch(url)

        traces = data.get("data", [])

        if not traces:
            return None

        return traces[0]
