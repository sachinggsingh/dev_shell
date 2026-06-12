import io
import unittest
from contextlib import redirect_stdout

from commands.network_commands import NetWorkcommands


class NetworkCommandsTests(unittest.TestCase):
    def test_ip_help_flag_prints_usage(self):
        command = NetWorkcommands()
        output = io.StringIO()

        with redirect_stdout(output):
            command.ip(["-h"])

        result = output.getvalue()
        self.assertIn("Usage: ip", result)
        self.assertIn("--help", result)

    def test_ip_all_flag_prints_addresses_for_localhost(self):
        command = NetWorkcommands()
        output = io.StringIO()

        with redirect_stdout(output):
            command.ip(["-a", "localhost"])

        result = output.getvalue()
        self.assertIn("Addresses", result)


if __name__ == "__main__":
    unittest.main()
