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

    def test_draft_state(self):
        self.assertFalse(can_export_report("account-1", "account-1", "draft"))

    def test_uppercase_ready_state(self):
        self.assertFalse(can_export_report("account-1", "account-1", "READY"))

    def test_empty_state(self):
        self.assertFalse(can_export_report("account-1", "account-1", ""))

    def test_none_state(self):
        self.assertFalse(can_export_report("account-1", "account-1", None))


if __name__ == "__main__":
    unittest.main()
