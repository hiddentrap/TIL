from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from servers.views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # Given Nothing

        # When
        found = resolve('/')

        # Then
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # Given
        request = HttpRequest()

        # When
        response = home_page(request)
        html = response.content.decode('utf8')

        # Then
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Asset Inventory</title>', html)
        self.assertTrue(html.endswith('</html>'))
