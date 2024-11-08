"""
URL configuration for car_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.urls import path,include

# urlpatterns = [
#     path('', admin.site.urls),
# ]

# path('', views.home, name='home')
from .views import UserLoginView,UserRegistrationView,HomeView,UserLogoutView,CarForSaleView,CarForRentView,CarForSaleDetailView,CarForRentDetailView,MyCarsForSaleView,MyCarsForRentView,  EditCarForSaleView, DeleteCarForSaleView,EditCarForRentView, DeleteCarForRentView,MyProfileView,EditMyProfileView,CarDetailView
from django.urls import path

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'), 
    path('logout/',UserLogoutView.as_view(),name = 'logout'),
    path('add_car_for_sale/',CarForSaleView.as_view(),name='add_car_for_sale'),
    path('car_for_rent/',CarForRentView.as_view(),name='car_for_rent'),
   
    path('car_for_sale_detail/', CarForSaleDetailView.as_view(), name='car_for_sale_detail'),
    path('car_for_rent_detail/', CarForRentDetailView.as_view(), name='car_for_rent_detail'),
    path('my_cars_for_sale/', MyCarsForSaleView.as_view(), name='my_cars_for_sale'),
    path('my_cars_for_rent/', MyCarsForRentView.as_view(), name='my_cars_for_rent'),
   
    path('edit-car-for-sale/<int:pk>/', EditCarForSaleView.as_view(), name='edit_car_for_sale'),
    path('delete-car-for-sale/<int:pk>/', DeleteCarForSaleView.as_view(), name='delete_car_for_sale'),
    path('edit-car-for-rent/<int:pk>/', EditCarForRentView.as_view(), name='edit_car_for_rent'),
    path('delete-car-for-rent/<int:pk>/', DeleteCarForRentView.as_view(), name='delete_car_for_rent'),

    path('my_profile/',MyProfileView.as_view(),name='my_profile'),
    path('edit_my_profile/',EditMyProfileView.as_view(),name='edit_my_profile'),
    path('car/<int:car_id>/', CarDetailView.as_view(), name='car_detail'),  # Detail view for a car
]
