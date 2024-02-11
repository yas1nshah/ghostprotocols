from django.urls import path
from .import views

urlpatterns = [
    #  ? get by stock ID
    path('cardetails/<int:stockid>', views.car_details),
    # path('login', views.login),
    # ? User
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('is-authenticated', views.isAuthenticatedView.as_view(),
         name='isAuthenticated'),
    path('my-cars', views.MyCarsView.as_view(), name='my-cars'),
    # ? Cars
    path('home', views.HomePageView.as_view(), name='home'),
    #     path('search', views.SearchPageView.as_view(), name='search'),
    path('inventory', views.FilterCarsView.as_view(), name='inventory'),
    # ? Post Cars
    path('add-car', views.PostCarView.as_view(), name='add-car'),
    path('add-car/gallery', views.GalleryUploadView.as_view(),
         name='add-car/gallery'),
    path('delete-gallery', views.DeleteGallery.as_view(),
         name='delete-gallery'),
     path('edit-car/<int:stockid>', views.EditCarView.as_view(), name='edit-car'),
    path('report', views.ReportCarView.as_view(), name='report'),
    # ? Manage!
    path('wesellyouwin', views.WeSellYouWinCreateView.as_view(), name='weSellYouWin'),
    path('demand-list', views.DemandListView.as_view(), name='demand-list'),

]
