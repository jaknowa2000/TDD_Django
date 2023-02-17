from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):
    # sprawdza czy istnieje mapowanie url do widoku home_page
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    # sprawdza czy zadanie zwraca odpowiedni kod przez widok
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Listy rzeczy do zrobienia</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
