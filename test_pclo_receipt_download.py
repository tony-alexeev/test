import unittest

from pclo_receipt_download import can_download_receipt


class CanDownloadReceiptTests(unittest.TestCase):
    def test_final_receipt_for_owner(self):
        self.assertTrue(can_download_receipt("account-1", "account-1", "final"))

    def test_different_requester(self):
        self.assertFalse(can_download_receipt("account-1", "account-2", "final"))

    def test_empty_ids(self):
        self.assertFalse(can_download_receipt("", "", "final"))
        self.assertFalse(can_download_receipt("", "account-1", "final"))
        self.assertFalse(can_download_receipt("account-1", "", "final"))


if __name__ == "__main__":
    unittest.main()
