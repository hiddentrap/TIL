import unittest

from contact import Contact


class ContactTests(unittest.TestCase):
    def test_something(self):
        kim = Contact('김일구', '010-8812-1193', 'ilgu.kim@python.com', 'Seoul')

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
