from django.shortcuts import render, redirect
from lists.models import Item, List
from django.http import HttpResponse # - zastepujemy lepszym - render


# tu utworzymy widoki
def home_page(request):
    return render(request, 'home.html')


def view_list(request, **kwargs):
    list_id = kwargs.get('list_id')
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)  # przekazanie szablonowi elementów z widoku strony głownej
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)  # automatycznie jest save
    return redirect(f'/lists/{list_.id}/')


def add_item(request, **kwargs):
    list_id = kwargs.get('list_id')
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

