from django.shortcuts import render
# from django.http import HttpResponse # - zastepujemy lepszym - render


# tu utworzymy widoki
def home_page(request):
    # return HttpResponse('<html><title>Listy rzeczy do zrobienia</title></html>') - zastepujemy lepszym
    return render(request, 'home.html')

