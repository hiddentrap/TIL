from django.http import HttpRequest
from django.template.loader import render_to_string
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
        self.assertIn('<h1>서버관리</h1>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_home_page_can_save_a_POST_request(self):
        # Given
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'SERVER01'

        # When
        response = home_page(request)

        # Then
        self.assertIn('SERVER01', response.content.decode())
        expected_html = render_to_string('servers.html', {'new_item_text': 'SERVER01'})
        print(expected_html)
        # self.assertEqual(expected_html, response.content.decode())

    def test_uses_home_template(self):
        # Given Nothing

        # When
        response = self.client.get('/')

        # Then
        self.assertTemplateUsed(response, 'servers.html')
