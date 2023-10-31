from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="CarDetail"),
    path("<str:title>/<int:id>", views.carDetail, name="CarDetail"),
    path('search/', views.search_car, name='search'),
    # path('', views.inventory, name= "AllInventory"),
    # path('home', views.home, name= "AllInventory")

]
