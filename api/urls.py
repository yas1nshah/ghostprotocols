from django.urls import path
from .import views

urlpatterns = [
    # path('', views.getData),
    # path('cardetails/<int:stockid>', views.carDetils),
    # path('login', views.login),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('search', views.SearchPageView.as_view(), name='search'),
    path('home', views.SearchPageView.as_view(), name='home'),
    path('add-car', views.PostCarView.as_view(), name='add-car'),
    path('add-car/gallery', views.GalleryUploadView.as_view(),
         name='add-car/gallery'),
]
