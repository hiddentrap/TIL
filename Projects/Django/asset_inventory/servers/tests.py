from django.urls import resolve
from django.test import TestCase
from servers.views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # When
        found = resolve('/')

        # Then
        self.assertEqual(found.func, home_page)
