"""Hem_Logistics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path
from logistics import views as logistics_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', logistics_view.index, name='index'),
    path('Home/', logistics_view.home, name='home'),
    path('login/', logistics_view.Login, name ='login'), 
    path('logout/', auth.LogoutView.as_view(next_page='home'), name ='logout'),
    path('Contact Us', logistics_view.contact_us,name='contact_us'), 
    
    path('Add Driver/', logistics_view.driver, name='driver'),
    path('Driver/', logistics_view.show_driver, name='show_driver'),
    path('update_driver/<int:id>', logistics_view.update_driver, name='update_driver'),
    path('edit_driver/<int:id>', logistics_view.edit_driver, name='edit_driver'),
    path('delete_driver/<int:id>', logistics_view.delete_driver, name='delete_driver'), 
    
    path('Add Trip Detail/', logistics_view.trip_detail, name='trip_detail'), 
    path('Trip Detail/', logistics_view.show_trip_detail, name='show_trip_detail'),
    path('update_trip_detail/<int:id>', logistics_view.update_trip_detail, name='update_trip_detail'),
    path('edit_trip_detail/<int:id>', logistics_view.edit_trip_detail, name='edit_trip_detail'),
    path('delete_trip_detail/<int:id>', logistics_view.delete_trip_detail, name='delete_trip_detail'), 
    path('favoriteAjax/', logistics_view.favorite_ajax, name='favoriteAjax'),

    path('Add Vehicle/', logistics_view.vehicle, name='vehicle'), 
    path('Vehicle/', logistics_view.show_vehicle, name='show_vehicle'),
    path('update_vehicle/<int:id>', logistics_view.update_vehicle, name='update_vehicle'),
    path('edit_vehicle/<int:id>', logistics_view.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<int:id>', logistics_view.delete_vehicle, name='delete_vehicle'), 
    
    path('Add Bank Detail/', logistics_view.bank_detail, name='bank_detail'), 
    path('Bank Detail/', logistics_view.show_bank_detail, name='show_bank_detail'),
    path('update_bank_detail/<int:id>', logistics_view.update_bank_detail, name='update_bank_detail'),
    path('edit_bank_detail/<int:id>', logistics_view.edit_bank_detail, name='edit_bank_detail'),
    path('delete_bank_detail/<int:id>', logistics_view.delete_bank_detail, name='delete_bank_detail'),

    path('PUC_Notifications/', logistics_view.PUC_notifications, name ='PUC_Notifications'), 
    path('License_Notifications/', logistics_view.license_notifications, name ='License_Notifications'), 
    path('Insurance_Notifications/', logistics_view.insurance_notifications, name ='Insurance_Notifications'), 

]
