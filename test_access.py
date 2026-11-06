import unittest
from access import can_view_report


class ReportAccessTests(unittest.TestCase):
    def test_owner_can_view(self):
        self.assertTrue(can_view_report('alice', 'alice'))

    def test_other_account_cannot_view(self):
        self.assertFalse(can_view_report('alice', 'bob'))

    def test_anonymous_cannot_view(self):
        self.assertFalse(can_view_report('alice', None))

    def test_empty_owner_and_requester_cannot_view(self):
        self.assertFalse(can_view_report('', ''))


if __name__ == '__main__':
    unittest.main()
