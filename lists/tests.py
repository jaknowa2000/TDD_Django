from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()  # ta nazwa tylko dlatego zeby uniknac kolizji z list z pythona
        list_.save()

        first_item = Item()
        first_item.text = 'Absolutnie pierwszy element'
        first_item.list = list_
        # zapisanie w bazie danych
        first_item.save()

        second_item = Item()
        second_item.text = 'Drugi element'
        second_item.list = list_
        second_item.save()

        # sprawdzenie co zapisało sie w bazie danych
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Drugi element')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/whatever/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_items(self):
        # typowa składnia testu (setup)
        list_ = List.objects.create()
        Item.objects.create(text='element 1', list=list_)
        Item.objects.create(text='element 2', list=list_)

        # exercise
        response = self.client.get('/lists/whatever/')

        # assert
        self.assertContains(response, 'element 1')
        self.assertContains(response, 'element 2')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'Nowy element listy'})
        # sprawdzenie czy obiekt zapisał sie w bazie danych
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element listy')

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'Nowy element listy'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/whatever/')

