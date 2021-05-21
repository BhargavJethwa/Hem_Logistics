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
from django.urls import path
from logistics import views as logistics_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', logistics_view.index, name='index'),
    path('Home/', logistics_view.home, name='home'), 
    path('Contact Us', logistics_view.contact_us,name='contact_us'), 
    path('Add Driver/', logistics_view.driver, name='driver'),
    path('Driver', logistics_view.show_driver, name='show_driver'),
    path('update_driver/<int:id>', logistics_view.update_driver, name='update_driver'),
    path('edit_driver/<int:id>', logistics_view.edit_driver, name='edit_driver'),
    path('delete_driver/<int:id>', logistics_view.delete_driver, name='delete_driver'), 
    path('Add Trip Detail/', logistics_view.trip_detail, name='trip_detail'), 
    path('Add Vehicle/', logistics_view.vehicle, name='vehicle'), 
    path('Add Bank Detail/', logistics_view.bank_detail, name='bank_detail'), 
]
