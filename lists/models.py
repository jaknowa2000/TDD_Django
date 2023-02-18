from django.db import models


# Create your models here.
# atrybut id w bazie jako klucz gł. jest domyślny reszte trzeba zdefiniowac
class Item(models.Model):
    text = models.TextField(default='')
