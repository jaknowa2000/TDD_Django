from django.shortcuts import render, redirect
from lists.models import Item
from django.http import HttpResponse # - zastepujemy lepszym - render


# tu utworzymy widoki
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text']) # automatycznie jest save
        return redirect('/lists/whatever/')
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()  # przekazanie szablonowi elementów z widoku strony głownej
    return render(request, 'list.html', {'items': items})
