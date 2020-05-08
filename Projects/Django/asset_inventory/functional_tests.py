from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def treaDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # When
        self.browser.get('http://localhost:8000')

        # Then
        self.assertIn('Asset Inventory', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
