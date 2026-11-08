import unittest

from pclo_invoice_download import can_download_invoice


class CanDownloadInvoiceTests(unittest.TestCase):
    def test_issued_invoice_for_same_account(self):
        self.assertTrue(can_download_invoice("account-1", "account-1", "issued"))

    def test_different_requester(self):
        self.assertFalse(can_download_invoice("account-1", "account-2", "issued"))

    def test_empty_ids(self):
        self.assertFalse(can_download_invoice("", "", "issued"))
        self.assertFalse(can_download_invoice("account-1", "", "issued"))
        self.assertFalse(can_download_invoice("", "account-1", "issued"))


if __name__ == "__main__":
    unittest.main()
