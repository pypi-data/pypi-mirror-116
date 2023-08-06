import os
import unittest
from dnastack import PublisherClient


def assert_has_property(self, obj, attribute):
    self.assertTrue(
        attribute in obj,
        msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
        % (obj, attribute),
    )


class TestClientLibraryDataConnectQueryCommand(unittest.TestCase):
    def setUp(self):
        self.publisher_client = PublisherClient(
            dataconnect_url=os.getenv("E2E_DATA_CONNECT_URI")
            or "https://collection-service.publisher.dnastack.com/collection/library/search/"
        )

    def test_variant_query(self):
        result = self.publisher_client.dataconnect.query(
            "SELECT * FROM covid.cloud.variants LIMIT 10"
        )
        self.assertIsNotNone(result)

        for item in result:
            assert_has_property(self, item, "start_position")
            assert_has_property(self, item, "end_position")
            assert_has_property(self, item, "reference_bases")
            assert_has_property(self, item, "alternate_bases")
            assert_has_property(self, item, "sequence_accession")

    def test_drs_url_query(self):
        result = self.publisher_client.dataconnect.query(
            "SELECT drs_url FROM covid.cloud.files LIMIT 10"
        )
        self.assertIsNotNone(result)

        for item in result:
            assert_has_property(self, item, "drs_url")

    def test_incorrect_column_query(self):
        with self.assertRaises(Exception) as cm:
            self.publisher_client.dataconnect.query(
                "SELECT invalid_column FROM covid.cloud.variants LIMIT 10"
            )

    def test_broken_query(self):
        with self.assertRaises(Exception) as cm:
            self.publisher_client.dataconnect.query("broken_query")
