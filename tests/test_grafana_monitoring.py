"""Tests for Grafana monitoring client and provider."""

import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

from dev_shell.monitoring.grafana_client import GrafanaClient
from dev_shell.monitoring.provider.grafana import GrafanaProvider


class GrafanaClientTests(unittest.TestCase):
    def test_extract_value_reads_latest_frame_value(self):
        payload = {
            "results": {
                "A": {
                    "frames": [
                        {
                            "data": {
                                "values": [[1, 2, 3], [0.1, 0.2, 0.42]],
                            }
                        }
                    ]
                }
            }
        }

        self.assertEqual(GrafanaClient._extract_value(payload), 0.42)

    def test_extract_value_raises_on_query_error(self):
        payload = {"results": {"A": {"error": "bad query"}}}

        with self.assertRaisesRegex(Exception, "bad query"):
            GrafanaClient._extract_value(payload)

    def test_query_requires_datasource_uid(self):
        client = GrafanaClient(config_path="/nonexistent/grafana.json")

        with self.assertRaisesRegex(Exception, "datasource UID"):
            client.query("up")

    @patch("dev_shell.monitoring.grafana_client.urllib.request.urlopen")
    def test_ping_returns_true_on_healthy_response(self, mock_urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({"database": "ok"}).encode("utf-8")
        response.__enter__.return_value = response
        mock_urlopen.return_value = response

        client = GrafanaClient(config_path="/nonexistent/grafana.json")
        self.assertTrue(client.ping())


class GrafanaProviderTests(unittest.TestCase):
    def test_get_summary_normalizes_cpu_to_percent(self):
        client = MagicMock()
        client.query.side_effect = [0.25, 1024, 10, 0.01, 0.5]

        provider = GrafanaProvider(client=client)
        summary = provider.get_summary("demo-job")

        self.assertEqual(summary["cpu"], 25.0)
        self.assertEqual(summary["memory"], 1024.0)
        client.query.assert_called()


class GrafanaCommandTests(unittest.TestCase):
    def test_ping_command_prints_reachable(self):
        provider = MagicMock()
        provider.ping.return_value = True

        from dev_shell.commands.monitor.grafana import GrafanaCommands

        command = GrafanaCommands(provider=provider)
        output = io.StringIO()

        with redirect_stdout(output):
            command.execute(["ping"])

        self.assertIn("reachable", output.getvalue())


if __name__ == "__main__":
    unittest.main()
