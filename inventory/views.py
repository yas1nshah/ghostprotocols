from datetime import datetime  # Import datetime module
from django.http import HttpResponse
from django.shortcuts import render
from .utils import format_mileage, format_price

# from .models import Car
# # Create your views here.
from base.models import Car, Gallery
from django.db.models import Q, Prefetch
from django.template import loader
from account.models import User
from django.http import JsonResponse
from user_agents import parse
from django.template.loader import render_to_string  # Import render_to_string


def home(request):
    # Use a different name for the to_attr parameter, e.g., 'car_gallery'
    GpCars = Car.objects.order_by(
        '-stockid').filter(gpcar=True, featured=False)[:8]

    FeaturedCars = Car.objects.order_by(
        '-stockid').filter(gpcar=False, featured=True)[:8]
    RecentCars = Car.objects.order_by(
        '-stockid').filter(gpcar=False, featured=False)[:8]

    for car in GpCars:
        car.gallery = Gallery.objects.filter(car=car)
        car.featImg = car.gallery[car.galleryIndex]
        car.mileage = format_mileage(car.mileage)
        car.price = format_price(car.price)

    print(GpCars[0].featImg)

    for car in FeaturedCars:
        car.gallery = Gallery.objects.filter(car=car)
        car.featImg = car.gallery[car.galleryIndex]
        car.mileage = format_mileage(car.mileage)
        car.price = format_price(car.price)
    print(FeaturedCars[0].featImg)

    for car in RecentCars:
        car.gallery = Gallery.objects.filter(car=car)
        car.featImg = car.gallery[car.galleryIndex]
        car.mileage = format_mileage(car.mileage)
        car.price = format_price(car.price)

    # Parse the user agent using django-user-agents
    user_agent = parse(request.META['HTTP_USER_AGENT'])

    # Check if the request comes from a mobile device
    is_mobile = user_agent.is_mobile

    # Choose the template based on the device type
    template_name = 'm.home.html' if is_mobile else 'home.html'

    context = {
        'gpcars': GpCars,
        'ftcars': FeaturedCars,
        'rcntcars': RecentCars,
        'hello': "hi"
    }

    # Use the loader to render the template
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request))


def carDetail(request, title, id):
    result = Car.objects.filter(stockid=id).first()
    gallery = Gallery.objects.filter(car=id).all()

    print(result.seller.acc_type)
    print(result.seller)

    # Check if the result exists
    if result:
        result.mileage = format_mileage(result.mileage)
        result.price = format_price(result.price)

    # Parse the user agent using django-user-agents
    user_agent = parse(request.META['HTTP_USER_AGENT'])

    # Check if the request comes from a mobile device
    is_mobile = user_agent.is_mobile

    # Choose the template based on the device type
    template_name = 'm.car_detail.html' if is_mobile else 'car_detail.html'

    context = {
        "details": result,
        "gallery": gallery,
    }

    return render(request, template_name, context)


def search_car(request):
    query = request.GET.get('keyword', '')
    query = query.replace("%20", " ")
    year_from = request.GET.get('yearFrom', 2000)
    year_to = request.GET.get('yearTo', 2023)
    price_from = request.GET.get('priceFrom', 0)
    price_to = request.GET.get('priceTo', 100000000)
    color = request.GET.get('color', '')
    body_type = request.GET.get('bodyType', '')

    # Create a list of conditions to filter cars
    conditions = [Q(year__gte=year_from) & Q(year__lte=year_to),
                  Q(price__gte=price_from) & Q(price__lte=price_to)]

    if query:
        conditions.append(Q(title__icontains=query) | Q(make__icontains=query) | Q(
            model__icontains=query) | Q(location__icontains=query))
    if color:
        conditions.append(Q(color__iexact=color))
    if body_type:
        conditions.append(Q(body__iexact=body_type))

    # Combine the conditions using the 'AND' operator
    results = Car.objects.filter(Q(*conditions))[:20]

    # Access gallery for each car in the results
    for car in results:
        car.gallery = Gallery.objects.filter(car=car)
        car.featImg = car.gallery[car.galleryIndex]
        car.mileage = format_mileage(car.mileage)
        car.price = format_price(car.price)

    print(results)
    # print(results[1].inspection)
    print(results[0].gallery[0])

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'search.html', context)


def about_us(request):
    return render(request, 'about_us.html')
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
