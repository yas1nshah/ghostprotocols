import statistics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Car, Gallery
#
# from django.contrib.auth import authenticate, login
# from django.contrib.auth import get_user_model
# from rest_framework.permissions import IsAuthenticated
# # from . import UserSerailizer

#
from api.serializers import UserProfileSerializer, UserRegistrationSerializer, AddCarSerializer, GallerySerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
# JWT TOKEN
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


# @api_view(["GET"])
# def getData(request):
#     person = {"hello": 'hi'}
#     return Response(person)


# @api_view(['GET'])
# def carDetils(request, stockid):
#     try:
#         carData = Car.objects.get(stockid=stockid)
#         print(carData.title)
#         carGalleryQuery = Gallery.objects.filter(car__stockid=stockid).all()
#         carGallery = []
#         for img in carGalleryQuery:
#             carGallery.append(img.image.url)
#         print(carGallery)
#         serialized_car = {
#             "stockid": carData.stockid,
#             'title': carData.title,
#             "gallery": carGallery,
#             "galleryIndex": carData.galleryIndex,
#             "make": carData.make,
#             "model": carData.model,
#             "year": carData.year,
#             "price": carData.price,
#             "location": carData.location,
#             "mileage": carData.mileage,
#             "transmission": carData.transmission,
#             "engine": carData.engine,
#             "registration": carData.registration,
#             "body": carData.body,
#             "color": carData.color,
#             "sellerComments": carData.sellerComments,
#             # Add more fields as needed
#         }
#         return Response(serialized_car)
#     except Car.DoesNotExist:
#         return Response({"error": "Car not found"}, status=404)


# @api_view(['POST'])
# def login(request):
#     # print(request.data['username'])
#     username = request.data["phone"]
#     password = request.data["password"]
#     user = authenticate(request, phone=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         return Response({'hi': 'sucess'})
#         # ...
#     else:
#         # Return an 'invalid login' error message.
#         # ...
#         return Response({'hi': 'failed'})


# generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            get_tokens_for_user(user)
            return Response({'msg': "reg sucessfull"})
        else:
            return Response({'msg': "reg failed"})


class UserLoginView(APIView):
    def post(self, request, format=None):
        # serializer = UserLoginSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        phone = request.data.get('phone')
        password = request.data.get('password')
        user = authenticate(
            request=request, phone=phone, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': "Login Sucessfull", "token": token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "The phone and passwords dont match"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'data': serializer.data})


class SearchPageView(APIView):
    def get(self, requst, format=None):
        return Response({'data': requst.data})


class HomePageView(APIView):
    def get(self, request, format=None):
        gpCars = Car.objects.filter(gpcar=True).order_by('-stockid')[:6]
        featuredCars = Car.objects.filter(
            featured=True).order_by('-stockid')[:6]
        recentCars = Car.objects.filter(
            gpcar=False, featured=False).order_by('-stockid')[:6]
        return Response()


class PostCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()  # Create a copy of the request data
        data["seller"] = request.user.id
        serializer = AddCarSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data': serializer.data})


class GalleryUploadView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = GallerySerializer(data=request.data)

        if serializer.is_valid():
            car_stockid = serializer.validated_data['car'].stockid
            try:
                car = Car.objects.get(stockid=car_stockid)
                if car.seller == request.user:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'You are not the owner of this car.'}, status=status.HTTP_403_FORBIDDEN)
            except Car.DoesNotExist:
                return Response({'error': 'Car not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
