# ? Modles
from base.models import Car, DemandList, Gallery
# ? Seializers
from api.serializers import CarReportSerializer, CarSerializer, DemandListSerializer, UserProfileSerializer, UserRegistrationSerializer, AddCarSerializer, GallerySerializer, WeSellYouWinSerializer
# ? Rest Frameworks
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken


# ? Get Car by Stock ID
@api_view(['GET'])
def carDetils(request, stockid):
    try:
        carData = Car.objects.get(stockid=stockid)
        print(carData.title)
        carGalleryQuery = Gallery.objects.filter(car__stockid=stockid).all()
        carGallery = []
        for img in carGalleryQuery:
            carGallery.append(img.image.url)
        print(carGallery)
        serialized_car = {
            "stockid": carData.stockid,
            'title': carData.title,
            "gallery": carGallery,
            "galleryIndex": carData.galleryIndex,
            "make": carData.make,
            "model": carData.model,
            "year": carData.year,
            "price": carData.price,
            "location": carData.location,
            "mileage": carData.mileage,
            "transmission": carData.transmission,
            "engine": carData.engine,
            "registration": carData.registration,
            "body": carData.body,
            "color": carData.color,
            "sellerComments": carData.sellerComments,
            # Add more fields as needed
        }
        return Response(serialized_car)
    except Car.DoesNotExist:
        return Response({"error": "Car not found"}, status=404)


# ! generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# ? User Registration


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': "Registered", "token": token})
        else:
            return Response({'msg': "Registeration Failed"})

# ? User Login


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


# ? Check For Login
class isAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"logged_in?": "yes"}, status=status.HTTP_200_OK)

# ? User Profile


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)

        return Response({'data': serializer.data})


# class SearchPageView(APIView):
#     def get(self, requst, format=None):
#         return Response({'data': requst.data})

#  # gpCars = Car.objects.filter(gpcar=True).order_by('-stockid')[:6]

#         # featuredCars = Car.objects.filter(
#         #     featured=True).order_by('-stockid')[:6]


# ? Home Page View
class HomePageView(APIView):

    def get(self, request, ):
        # Fetch the first 5 Car objects
        GpCars = Car.objects.order_by(
            '-stockid').filter(gpcar=False, featured=False)[:6]
        FeaturedCars = Car.objects.order_by(
            '-stockid').filter(gpcar=False, featured=False)[:6]
        RecentCars = Car.objects.order_by(
            '-stockid').filter(gpcar=False, featured=False)[:6]

        # Serialize the queryset
        gpSerial = CarSerializer(GpCars, many=True)
        featSerial = CarSerializer(FeaturedCars, many=True)
        RecentSerial = CarSerializer(RecentCars, many=True)

        return Response({"gpcars": gpSerial.data, "featuredCars": featSerial.data, "recentcars": RecentSerial.data}, status=status.HTTP_200_OK)


# ? Post Car View
class PostCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user

        # Check if the user has reached their ad limit
        if user.ad_limit > 0:
            existing_cars = Car.objects.filter(seller=user).count()
            if existing_cars >= user.ad_limit:
                return Response(
                    {"error": "You have reached your car posting limit."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data = request.data.copy()  # Create a copy of the request data
        data["seller"] = user.id
        serializer = AddCarSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data': serializer.data})

# ? Gallery Upload View


class GalleryUploadView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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


# ? Report Car View
class ReportCarView(APIView):
    def post(self, request):
        serializer = CarReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Car Reported"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ? My Cars View
class MyCarsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        items_per_page = 5
        starting_index = (page - 1) * items_per_page
        ending_index = page * items_per_page
        myCars = Car.objects.order_by(
            '-stockid').filter(seller=request.user)[starting_index:ending_index]
        myCarsSerial = CarSerializer(myCars, many=True)

        return Response({"mycars": myCarsSerial.data})


# ? Search Result with Filter
class FilterCarsView(APIView):
    def post(self, request):
        data = request.data

        location = data.get('location', 'All')
        print(location)
        make = data.get('make', 'All')
        model = data.get('model', 'All')
        year_range = data.get('year', 'All')
        price_range = data.get('price', 'All')
        registration = data.get('registration', 'All')
        transmission = data.get('transmission', 'All')
        page = int(data.get('page', 1))

        # Build the filter conditions based on provided parameters
        filter_conditions = {}
        if location != 'All Cities':
            filter_conditions['location'] = location
        if make != 'All Makes':
            filter_conditions['make'] = make
        if model != 'All Models':
            filter_conditions['model'] = model
        if registration != 'All Registrations':
            filter_conditions['registration'] = registration
        if transmission != 'All':
            filter_conditions['transmission'] = transmission

        # Handle year range filtering
        if year_range != 'All Years':
            start_year, end_year = map(int, year_range.split('-'))
            filter_conditions['year__gte'] = start_year
            filter_conditions['year__lte'] = end_year

        # Handle price range filtering
        if price_range != 'All Prices':
            start_price, end_price = map(int, price_range.split('-'))
            filter_conditions['price__gte'] = start_price
            filter_conditions['price__lte'] = end_price

        # print(**filter_conditions)
        items_per_page = 15
        starting_index = (page - 1) * items_per_page
        ending_index = page * items_per_page

        # Apply filters and paginate the results
        cars = Car.objects.order_by('-stockid').filter(
            **filter_conditions)[starting_index:ending_index]

        # Serialize the queryset
        serializer = CarSerializer(cars, many=True)

        return Response(serializer.data)


# ? We Sell You Win
class WeSellYouWinCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {'user': user.id, }
        serializer = WeSellYouWinSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ? Demand List View
class DemandListView(APIView):
    def post(self, request):
        page = int(request.data.get('page', 1))
        items_per_page = 10
        starting_index = (page - 1) * items_per_page
        ending_index = page * items_per_page

        # Apply filters and paginate the results
        demand_list = DemandList.objects.filter(
            done=False).order_by('-id')[starting_index:ending_index]
        print(demand_list)

        # Use many=True for serializing a list of objects
        serializer = DemandListSerializer(demand_list, many=True)
        # if serializer.is_valid():
        return Response({"demandList": serializer.data}, status=status.HTTP_200_OK)
