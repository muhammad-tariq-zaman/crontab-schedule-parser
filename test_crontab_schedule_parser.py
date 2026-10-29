import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import parse_line, describe_field


class TestCrontabParser(unittest.TestCase):
    def test_every_minute(self):
        self.assertEqual(parse_line("* * * * * /bin/true")["description"].split(";")[0],
                         "every minute")

    def test_step_value(self):
        self.assertIn("every 15 minutes", parse_line("*/15 * * * * job")["description"])

    def test_comments_and_env_skipped(self):
        self.assertIsNone(parse_line("# comment"))
        self.assertIsNone(parse_line("PATH=/usr/bin"))

    def test_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            parse_line("99 * * * * job")


if __name__ == "__main__":
    unittest.main()
