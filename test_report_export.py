import unittest

from report_export import can_export_report


class CanExportReportTests(unittest.TestCase):
    def test_ready_owner(self):
        self.assertTrue(can_export_report("account-1", "account-1", "ready"))

    def test_different_requester(self):
        self.assertFalse(can_export_report("account-1", "account-2", "ready"))

    def test_empty_ids(self):
        self.assertFalse(can_export_report("", "", "ready"))
        self.assertFalse(can_export_report("", "account-1", "ready"))
        self.assertFalse(can_export_report("account-1", "", "ready"))


if __name__ == "__main__":
    unittest.main()
