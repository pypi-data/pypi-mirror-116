import os
import unittest
from click.testing import CliRunner
import json
from dnastack import __main__ as cli


class TestCliConfigCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.data_connect_url = (
            os.getenv("E2E_DATA_CONNECT_URI")
            or "https://collection-service.publisher.dnastack.com/collection/library/search/"
        )

    def test_cli_config_add_config_and_list(self):
        result = self.runner.invoke(
            cli.dnastack, ["config", "set", "testKey", "testValue"]
        )

        self.assertEqual(result.exit_code, 1)

        self.runner.invoke(
            cli.dnastack,
            [
                "config",
                "set",
                "data-connect-url",
                self.data_connect_url,
            ],
        )

        result = self.runner.invoke(cli.dnastack, ["config", "list"])

        result_object = json.loads(result.output)

        self.assertEqual(result_object["data-connect-url"], self.data_connect_url)
