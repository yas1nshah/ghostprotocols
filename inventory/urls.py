from django.urls import path

from . import views

urlpatterns = [
    path("<str:makeq>", views.carDetail, name= "CarDetail")
]
