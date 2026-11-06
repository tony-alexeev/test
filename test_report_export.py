import unittest

from report_export import can_export_report


class ReportExportTests(unittest.TestCase):
    def test_ready_owner_can_export(self):
        self.assertTrue(can_export_report("account-1", "account-1", "ready"))

    def test_different_requester_cannot_export(self):
        self.assertFalse(can_export_report("account-1", "account-2", "ready"))

    def test_empty_ids_cannot_export(self):
        for owner_id, requester_id in (("", "account-1"), ("account-1", ""), ("", "")):
            with self.subTest(owner_id=owner_id, requester_id=requester_id):
                self.assertFalse(can_export_report(owner_id, requester_id, "ready"))


if __name__ == "__main__":
    unittest.main()
