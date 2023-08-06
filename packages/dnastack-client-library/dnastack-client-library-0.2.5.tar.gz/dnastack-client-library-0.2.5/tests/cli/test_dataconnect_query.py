import os
import unittest
from click.testing import CliRunner
import json
import csv
from io import StringIO
from dnastack import __main__ as cli


def assert_has_property(self, obj, attribute):
    self.assertTrue(
        attribute in obj,
        msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
        % (obj, attribute),
    )


class TestCliDataConnectQueryCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.data_connect_url = (
            os.getenv("E2E_DATA_CONNECT_URI")
            or "https://collection-service.publisher.dnastack.com/collection/library/search/"
        )
        self.runner.invoke(
            cli.dnastack,
            [
                "config",
                "set",
                "data-connect-url",
                self.data_connect_url,
            ],
        )

    def test_variant_query(self):
        result = self.runner.invoke(
            cli.dnastack,
            ["dataconnect", "query", "SELECT * FROM covid.cloud.variants LIMIT 10"],
        )
        result_objects = json.loads(result.output)

        self.assertEqual(result.exit_code, 0)

        for item in result_objects:
            assert_has_property(self, item, "start_position")
            assert_has_property(self, item, "end_position")
            assert_has_property(self, item, "reference_bases")
            assert_has_property(self, item, "alternate_bases")
            assert_has_property(self, item, "sequence_accession")

    def test_csv_query(self):
        result = self.runner.invoke(
            cli.dnastack,
            [
                "dataconnect",
                "query",
                "SELECT * FROM covid.cloud.variants LIMIT 10",
                "-f",
                "csv",
            ],
        )
        csv_string = StringIO(result.output)
        csv_results = csv.reader(csv_string)

        self.assertEqual(result.exit_code, 0)

        header_row = next(csv_results)

        # tests that headers are present
        self.assertIn("start_position", header_row)
        self.assertIn("end_position", header_row)
        self.assertIn("reference_bases", header_row)
        self.assertIn("alternate_bases", header_row)
        self.assertIn("sequence_accession", header_row)

        for item in csv_results:
            self.assertEqual(len(item), len(header_row))

    def test_drs_url_query(self):
        result = self.runner.invoke(
            cli.dnastack,
            ["dataconnect", "query", "SELECT drs_url FROM covid.cloud.files LIMIT 10"],
        )
        result_objects = json.loads(result.output)

        self.assertEqual(result.exit_code, 0)

        for item in result_objects:
            assert_has_property(self, item, "drs_url")

    def test_incorrect_column_query(self):
        result = self.runner.invoke(
            cli.dnastack,
            [
                "dataconnect",
                "query",
                "SELECT imaginary_field FROM covid.cloud.variants LIMIT 10",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Column 'imaginary_field' cannot be resolved", result.output)

    def test_broken_query(self):
        result = self.runner.invoke(
            cli.dnastack, ["dataconnect", "query", "broken_query"]
        )
        self.assertEqual(result.exit_code, 1)
