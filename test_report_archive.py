import unittest

from report_archive import can_archive_report


class CanArchiveReportTests(unittest.TestCase):
    def test_closed_report_with_matching_ids(self):
        self.assertTrue(can_archive_report("account-1", "account-1", "closed"))

    def test_different_ids(self):
        self.assertFalse(can_archive_report("account-1", "account-2", "closed"))

    def test_empty_ids(self):
        for owner_id, requester_id in (("", "account-1"), ("account-1", ""), ("", "")):
            with self.subTest(owner_id=owner_id, requester_id=requester_id):
                self.assertFalse(can_archive_report(owner_id, requester_id, "closed"))

    def test_ready_report(self):
        self.assertFalse(can_archive_report("account-1", "account-1", "ready"))

    def test_uppercase_closed(self):
        self.assertFalse(can_archive_report("account-1", "account-1", "CLOSED"))


if __name__ == "__main__":
    unittest.main()
