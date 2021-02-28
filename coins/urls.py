from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('coins-list/', views.get_coins_list, name='coins_list'),
]