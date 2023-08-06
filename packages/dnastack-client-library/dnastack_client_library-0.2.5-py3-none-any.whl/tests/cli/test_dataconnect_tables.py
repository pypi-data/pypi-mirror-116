import os
import unittest
from click.testing import CliRunner
import json
from dnastack import __main__ as cli


def assert_has_property(self, obj, attribute):
    self.assertTrue(
        attribute in obj,
        msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
        % (obj, attribute),
    )


class TestCliDataConnectTablesCommand(unittest.TestCase):
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

    def test_tables_list(self):
        result = self.runner.invoke(cli.dnastack, ["dataconnect", "tables", "list"])
        result_objects = json.loads(result.output)

        self.assertEqual(result.exit_code, 0)

        for item in result_objects:
            assert_has_property(self, item, "name")
            assert_has_property(self, item, "data_model")
            assert_has_property(self, item["data_model"], "$ref")

    def test_tables_get_table(self):
        table_list_result = self.runner.invoke(
            cli.dnastack, ["dataconnect", "tables", "list"]
        )
        result_objects = json.loads(table_list_result.output)

        table_name = result_objects[len(result_objects) - 1]["name"]

        table_info_result = self.runner.invoke(
            cli.dnastack, ["dataconnect", "tables", "get", table_name]
        )
        table_info_object = json.loads(table_info_result.output)

        self.assertEqual(table_info_result.exit_code, 0)

        assert_has_property(self, table_info_object, "name")
        assert_has_property(self, table_info_object, "description")
        assert_has_property(self, table_info_object, "data_model")
        assert_has_property(self, table_info_object["data_model"], "$id")
        assert_has_property(self, table_info_object["data_model"], "$schema")
        assert_has_property(self, table_info_object["data_model"], "description")

        for property in table_info_object["data_model"]["properties"]:
            assert_has_property(
                self, table_info_object["data_model"]["properties"][property], "format"
            )
            assert_has_property(
                self, table_info_object["data_model"]["properties"][property], "type"
            )
            assert_has_property(
                self,
                table_info_object["data_model"]["properties"][property],
                "$comment",
            )

    def test_tables_get_table_does_not_exist(self):
        table_info_result = self.runner.invoke(
            cli.dnastack, ["dataconnect", "tables", "get", "some table name"]
        )

        self.assertEqual(table_info_result.exit_code, 1)
