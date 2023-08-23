from django.http import HttpResponse
from django.shortcuts import render

# from .models import Car
# # Create your views here.

# def carDetail(request, make, model, year, id):
#     query = Car.objects.filter(id = id).first()
#     # print(query)
#     return render(request, 'car_detail.html')

# def inventory(request):
#     query = Car.objects.all()[:8]
#     # return render(request, )
#     print(query[0].make)
#     print(query[1].model)
#     # return HttpResponse(f'{query[0].make} {query[0].model} {query[0].year}')
#     return render(request, 'inventory.html', {'data':query})

# def home(request):
#     query = Car.objects.all()[:8]
#     return render(request, 'home.html', {'data':query})
