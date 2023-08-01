from django.http import HttpResponse
from django.shortcuts import render

from .models import Car
# Create your views here.

def carDetail(request, makeq):
    query = Car.objects.filter(make = makeq).all()
    print(query)

    return HttpResponse(f"HELLO WORLD {makeq}")