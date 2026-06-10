import json
import urllib.request
import urllib.parse
import urllib.error
import os

class PrometheusClient:
    def __init__(self, config_path="config/prometheus.json"):
        self.host = "localhost"
        self.port = 9090
        self._load_config(config_path)
        self.base_url = f"http://{self.host}:{self.port}/api/v1/query"

    def _load_config(self, config_path):
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    self.host = config.get("host", "localhost")
                    self.port = config.get("port", 9090)
            except Exception as e:
                print(f"Warning: Failed to load Prometheus config: {e}")

    def query(self, promql_query):
        """Execute a PromQL query and return the value."""
        params = urllib.parse.urlencode({'query': promql_query})
        url = f"{self.base_url}?{params}"
        
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read())
                
                if data.get("status") == "success":
                    result = data.get("data", {}).get("result", [])
                    if result:
                        # Return the value from the first result
                        # value is usually [timestamp, "value_string"]
                        return result[0].get("value", [None, None])[1]
                return None
        except urllib.error.URLError as e:
            raise Exception(f"Failed to connect to Prometheus: {e}")
        except Exception as e:
            raise Exception(f"Query failed: {e}")
