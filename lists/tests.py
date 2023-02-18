from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'Nowy element listy'})
        # sprawdzenie czy obiekt zapisał sie w bazie danych
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element listy')

    def test_redirect_after_POST(self):
        response = self.client.post('/', data={'item_text': 'Nowy element listy'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_list_items(self):
        # typowa składnia testu (setup)
        Item.objects.create(text='element 1')
        Item.objects.create(text='element 2')

        # exercise
        response = self.client.get('/')

        # assert
        self.assertIn('element 1', response.content.decode())
        self.assertIn('element 2', response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'Absolutnie pierwszy element'
        # zapisanie w bazie danych
        first_item.save()

        second_item = Item()
        second_item.text = 'Drugi element'
        second_item.save()

        # sprawdzenie co zapisało sie w bazie danych
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element')
        self.assertEqual(second_saved_item.text, 'Drugi element')