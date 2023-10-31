from datetime import datetime  # Import datetime module
from django.http import HttpResponse
from django.shortcuts import render
from .utils import format_mileage, format_price

# from .models import Car
# # Create your views here.
from base.models import Car, Gallery
from django.db.models import Q, Prefetch
from account.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string  # Import render_to_string


def home(request):
    # Use a different name for the to_attr parameter, e.g., 'car_gallery'
    GpCars = Car.objects.order_by(
        '-stockid')[:8]
    GpCars = GpCars.prefetch_related(
        Prefetch('gallery_set', queryset=Gallery.objects.all(), to_attr='car_gallery'))
    # for car in GpCars:
    # print(car.car_gallery[0].image)

    FeaturedCars = Car.objects.order_by(
        '-stockid').filter(gpcar=False, featured=False)[:8]
    RecentCars = Car.objects.order_by(
        '-stockid').filter(gpcar=False, featured=False)[:8]

    context = {
        'gpcars': GpCars,
        'ftcars': FeaturedCars,
        'rcntCars': RecentCars,
        'hello': "hi"
    }

    return render(request, 'home.html', context)


def carDetail(request, title, id):
    result = Car.objects.filter(stockid=id).first()
    gallery = Gallery.objects.filter(car=id).all()

    print(result.seller.acc_type)
    print(result.seller)

    # Check if the result exists
    if result:
        result.mileage = format_mileage(result.mileage)
        result.price = format_price(result.price)

    context = {
        "details": result,
        "gallery": gallery,
    }
    return render(request, 'car_detail.html', context)


def search_car(request):
    query = request.GET.get('q', '')
    # Add more filter parameters here
    results = Car.objects.filter(title__icontains=query)

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'search.html', context)

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
