# ? Modles
from base.models import Car, DemandList, Gallery
# ? Seializers
from api.serializers import CarReportSerializer, CarSerializer, DemandListSerializer, UserProfileSerializer, UserRegistrationSerializer, AddCarSerializer, GallerySerializer, WeSellYouWinSerializer
# ? Rest Frameworks
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.db.models import Q

# ? Get Car by Stock ID
@api_view(['GET'])
def car_details(request, stockid):
    car_data = get_object_or_404(Car, stockid=stockid)
    serializer = CarSerializer(car_data)
    return Response(serializer.data, status=200)


# ! generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class EditCarView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
    
    def get_car(self, stockid):
        return get_object_or_404(Car, stockid=stockid)
    
    def check_permissions(self, seller):
        user = self.request.user
        return user == seller or user.is_staff

    
    def get(self, request, stockid, format=None):
        try:
            car_data = self.get_car(stockid)
            print(car_data.seller)
            if not self.check_permissions(car_data.seller):
                return Response({"error": "You are not authorized to view this car"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = CarSerializer(car_data)
            return Response(serializer.data)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, stockid, format=None):
        try:
            car_data = self.get_car(stockid)
            if not self.check_permissions(car_data.seller):
                return Response({"error": "You are not authorized to update this car"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = CarSerializer(car_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

# ? User Registration
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': "Registered", "token": token}, status=201)  # 201 Created
        else:
            return Response({'errors': serializer.errors, 'msg': "Registration failed"}, status=400)

# ? User Login


class UserLoginView(APIView):
    def post(self, request, format=None):
        phone = request.data.get('phone')
        password = request.data.get('password')
        
        if not phone or not password:
            return Response({'error': "Phone and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request=request, phone=phone, password=password)
        
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': "Login Successful", "token": token}, status=status.HTTP_200_OK)
        else:
            # Use constant time comparison for security
            # This line is optional as Django's authenticate function already uses constant time comparison
            # but it's good to explicitly mention it for clarity and future-proofing.
            # https://docs.djangoproject.com/en/stable/topics/auth/passwords/#timing-attacks
            # if not user or not user.check_password(password):
            return Response({'error': "Invalid phone or password"}, status=status.HTTP_401_UNAUTHORIZED)


# ? Check For Login
class isAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"logged_in?": "yes"}, status=status.HTTP_200_OK)

# ? User Profile


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, format=None):
        user = self.get_object()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        user = self.get_object()
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "Profile updated successfully", 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SearchPageView(APIView):
#     def get(self, requst, format=None):
#         return Response({'data': requst.data})

#  # gpCars = Car.objects.filter(gpcar=True).order_by('-stockid')[:6]

#         # featuredCars = Car.objects.filter(
#         #     featured=True).order_by('-stockid')[:6]


# ? Home Page View
class HomePageView(APIView):

    def get(self, request):
        try:
            # Fetch the first 6 Car objects for each category
            gpcars = Car.objects.filter(gpcar=True, featured=False).order_by('-stockid')[:6]
            featured_cars = Car.objects.filter(gpcar=False, featured=True).order_by('-stockid')[:6]
            recent_cars = Car.objects.filter(gpcar=False, featured=False).order_by('-stockid')[:6]

            # Serialize the queryset
            gp_serial = CarSerializer(gpcars, many=True)
            feat_serial = CarSerializer(featured_cars, many=True)
            recent_serial = CarSerializer(recent_cars, many=True)

            return Response({"gpcars": gp_serial.data, "featuredCars": feat_serial.data, "recentcars": recent_serial.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ? Post Car View
class PostCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user

        # Uncomment and implement the ad limit check if necessary
        # if user.ad_limit > 0:
        #     existing_cars = Car.objects.filter(seller=user).count()
        #     if existing_cars >= user.ad_limit:
        #         return Response(
        #             {"error": "You have reached your car posting limit."},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )

        data = request.data.copy()  # Create a copy of the request data
        data["seller"] = user.id

        serializer = AddCarSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': "Car posted successfully", 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': "Failed to post car", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# ? Gallery Upload View

class DeleteGallery(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    def check_permissions(self, seller):
        user = self.request.user
        return user == seller or user.is_staff

    def delete(self, request, format=None):
        car_id = request.data.get('car_id')  # Assuming car_id is passed in the request body
        if car_id is not None:
            car = get_object_or_404(Car, pk=car_id)
            if not self.check_permissions(car.seller):
                return Response({'error': 'You are not authorized to delete gallery images for this car.'}, status=status.HTTP_403_FORBIDDEN)
            Gallery.objects.filter(car=car).delete()
            return Response({'message': 'Gallery images deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Car ID is missing in the request body.'}, status=status.HTTP_400_BAD_REQUEST)

class GalleryUploadView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]
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
    
    def get(self, request):
        keyword = request.GET.get('keyword', 'All')
        location = request.GET.get('location', 'All')
        make = request.GET.get('make', 'All')
        model = request.GET.get('model', 'All')
        year_from = request.GET.get('yearFrom', 'All')
        year_to = request.GET.get('yearTo', 'All')
        price_From = request.GET.get('priceFrom', 'All')
        price_To = request.GET.get('priceTo', 'All')
        registration = request.GET.get('registration', 'All')
        transmission = request.GET.get('transmission', 'All')
        body_type = request.GET.get("bodyType", 'All')
        ad_type = request.GET.get("adType",'All')
        page = int(request.GET.get('page', 1))

        filter_conditions = Q()

        if location != 'All':
            filter_conditions &= Q(location__iexact=location)
        if make != 'All':
            filter_conditions &= Q(make__iexact=make)
        if model != 'All':
            filter_conditions &= Q(model__iexact=model)
        if registration != 'All':
            filter_conditions &= Q(registration__iexact=registration)
        if transmission != 'All':
            filter_conditions &= Q(transmission=(transmission == 'Automatic'))
        
        if year_from != 'All':
            filter_conditions &= Q(year__gte=year_from)
        if year_to != 'All':
            filter_conditions &= Q(year__lte=year_to)
        
        if price_From != 'All':
            filter_conditions &= Q(price__gte= price_From)
        if price_To != 'All':
            filter_conditions &= Q(price__lte= price_To)
            
        
        if keyword != 'All':
            filter_conditions &= Q(title__icontains=keyword)
        
        if body_type != 'All':
            filter_conditions &= Q(body__iexact=body_type)
        
        if ad_type != 'All':
            if ad_type == "ghost-yard":
                filter_conditions &= Q(gpcar=True)
            elif ad_type == "featured":
                filter_conditions &= Q(featured=True)
            elif ad_type == "free-listing":
                filter_conditions &= Q(featured=False, gpcar=False)

        items_per_page = 20
        starting_index = (page - 1) * items_per_page
        ending_index = page * items_per_page

        cars = Car.objects.filter(filter_conditions).order_by('-stockid')[starting_index:ending_index]
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
    def get(self, request):
        # Get the page parameter from the query string or default to 1
        page = int(request.query_params.get('page', 1))
        items_per_page = 10
        starting_index = (page - 1) * items_per_page
        ending_index = page * items_per_page

        # Apply filters and paginate the results
        demand_list = DemandList.objects.filter(
            done=False).order_by('-id')[starting_index:ending_index]

        # Use many=True for serializing a list of objects
        serializer = DemandListSerializer(demand_list, many=True)

        return Response({"demandList": serializer.data}, status=status.HTTP_200_OK)
    
    
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
