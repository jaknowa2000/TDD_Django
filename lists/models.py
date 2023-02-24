from django.db import models


# Create your models here.
# atrybut id w bazie jako klucz gł. jest domyślny reszte trzeba zdefiniowac
class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default='')

