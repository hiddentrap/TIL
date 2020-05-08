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
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>서버관리</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_uses_home_template(self):
        # Given Nothing

        # When
        response = self.client.get('/')

        # Then
        self.assertTemplateUsed(response, 'servers.html')
