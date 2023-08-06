import os
import unittest
import pathlib
from dnastack import PublisherClient


class TestClientLibraryFilesCommand(unittest.TestCase):
    def setUp(self):
        self.publisher_client = PublisherClient(
            dataconnect_url=os.getenv("E2E_DATA_CONNECT_URI")
            or "https://collection-service.publisher.dnastack.com/collection/library/search/"
        )

    def test_drs_download(self):
        self.publisher_client.download(
            urls=[
                "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-b736-7868f559c795"
            ],
            output_dir="out",
        )
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").exists())

        # clean up ./out directory
        pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_multiple_drs_download(self):
        self.publisher_client.download(
            urls=[
                "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-b736-7868f559c795",
                "drs://drs.international.covidcloud.ca/2dc29273-ebac-49ec-b452-7d835abfa94b",
                "drs://drs.international.covidcloud.ca/e374d7ff-8944-4a6c-944b-78d40dd96654",
            ],
            output_dir="out",
        )

        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").exists())
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/SRR13820545.fa").exists())
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/SRR13820554.fa").exists())

        # clean up ./out directory
        pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out/SRR13820545.fa").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out/SRR13820554.fa").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_drs_download_from_broken_url(self):
        with self.assertRaises(Exception) as cm:
            self.publisher_client.download(
                urls=[
                    "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-BROKEN-b736-7868f559c795"
                ]
            )

    def test_drs_load(self):
        resource_url = (
            "drs://drs.international.covidcloud.ca/f5ff16d5-6be8-425c-acb5-8edbf023db52"
        )
        data = self.publisher_client.load([resource_url])

        self.assertIsNotNone(data)

    def test_drs_load_broken_url(self):
        with self.assertRaises(Exception) as cm:
            resource_url = "drs://drs.international.covidcloud.ca/f5ff16d5-6be8-425c-BROKEN-acb5-8edbf023db52"
            self.publisher_client.load([resource_url])
