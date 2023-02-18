from django.shortcuts import render
from django.http import HttpResponse # - zastepujemy lepszym - render


# tu utworzymy widoki
def home_page(request):
    return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', '')})

