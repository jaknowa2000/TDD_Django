"""TDD_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
# importuje widoki w mojej apki
from lists import views

urlpatterns = [
    # utworzenie polaczenia miedzy url '' a widokiem home_page
    path('<str:list_id>/', views.view_list, name='view_list'),
    path('new', views.new_list, name='new_list'),
    path('<str:list_id>/add_item', views.add_item, name='add_item')
]
