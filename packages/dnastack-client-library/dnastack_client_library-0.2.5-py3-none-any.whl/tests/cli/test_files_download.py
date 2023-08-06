import os
import unittest
from click.testing import CliRunner
import pathlib
from dnastack import __main__ as cli


class TestCliFilesCommand(unittest.TestCase):
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

    def test_drs_download(self):
        result = self.runner.invoke(
            cli.dnastack,
            [
                "files",
                "download",
                "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-b736-7868f559c795",
                "-o",
                "out",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").exists())

        # clean up ./out directory
        pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_multiple_drs_download(self):
        result = self.runner.invoke(
            cli.dnastack,
            [
                "files",
                "download",
                "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-b736-7868f559c795",
                "drs://drs.international.covidcloud.ca/2dc29273-ebac-49ec-b452-7d835abfa94b",
                "drs://drs.international.covidcloud.ca/e374d7ff-8944-4a6c-944b-78d40dd96654",
                "-o",
                "out",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").exists())
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/SRR13820545.fa").exists())
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/SRR13820554.fa").exists())

        # clean up ./out directory
        pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out/SRR13820545.fa").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out/SRR13820554.fa").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_input_file_flag_drs_download(self):
        input_file = open("download_input_file.txt", "w")
        input_file.write(
            "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-b736-7868f559c795\n"
            "drs://drs.international.covidcloud.ca/2dc29273-ebac-49ec-b452-7d835abfa94b\n"
            "drs://drs.international.covidcloud.ca/e374d7ff-8944-4a6c-944b-78d40dd96654"
        )
        input_file.close()

        result = self.runner.invoke(
            cli.dnastack,
            [
                "files",
                "download",
                "-i",
                pathlib.Path("./download_input_file.txt"),
                "-o",
                "out",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").exists())
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/SRR13820545.fa").exists())
        self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/SRR13820554.fa").exists())

        # # clean up ./out directory
        pathlib.Path(f"{os.getcwd()}/download_input_file.txt").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out/MW592874.fasta").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out/SRR13820545.fa").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out/SRR13820554.fa").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_drs_download_from_broken_url(self):
        result = self.runner.invoke(
            cli.dnastack,
            [
                "files",
                "download",
                "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-BROKEN-b736-7868f559c795",
                "-o",
                "out",
            ],
        )
        self.assertIn(
            "Could not get drs object id from url drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-BROKEN-b736-7868f559c795",
            result.output,
        )
