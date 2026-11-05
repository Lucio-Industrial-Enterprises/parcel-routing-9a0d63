import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_quotes(self):
        for zone, standard, express in (("local", "$8.00\n", "$15.00\n"),
                                        ("regional", "$11.00\n", "$18.00\n")):
            for options, expected in (([], standard),
                                      (["--service", "standard"], standard),
                                      (["--service", "express"], express)):
                with self.subTest(zone=zone, options=options):
                    result = subprocess.run(
                        [sys.executable, "-m", "warehouse.cli", "2", zone, *options],
                        capture_output=True, text=True, check=True,
                    )
                    self.assertEqual(result.stdout, expected)
                    self.assertEqual(result.stderr, "")

    def test_unknown_service(self):
        result = subprocess.run(
            [sys.executable, "-m", "warehouse.cli", "2", "local",
             "--service", "overnight"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid choice", result.stderr)
        self.assertIn("overnight", result.stderr)
