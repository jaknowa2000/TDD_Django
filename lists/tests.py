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
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{str(list_.id)}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        # typowa składnia testu (setup)
        correct_list = List.objects.create()
        Item.objects.create(text='element 1', list=correct_list)
        Item.objects.create(text='element 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='element pierwszy innej listy', list=other_list)
        Item.objects.create(text='element drugi innej listy', list=other_list)

        # exercise
        response = self.client.get(f'/lists/{correct_list.id}/')

        # assert
        self.assertContains(response, 'element 1')
        self.assertContains(response, 'element 2')
        self.assertNotContains(response, 'element pierwszy innej listy')
        self.assertNotContains(response, 'element drugi innej listy')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list, 'witam')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'Nowy element listy'})
        # sprawdzenie czy obiekt zapisał sie w bazie danych
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element listy')

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'Nowy element listy'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    def test_can_save_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'Nowy element dla istniejącej listy'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element dla istniejącej listy')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'Nowy element dla istniejącej listy'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
