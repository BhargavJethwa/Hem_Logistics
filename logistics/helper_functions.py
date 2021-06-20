from .models import Vehicle,Driver
from django.utils.timezone import now
from datetime import timedelta
def check_expiry_PUC():
    vehicles = Vehicle.objects.all()

    for vehicle in vehicles:
        if(vehicle.Notifications):
            if (vehicle.PUC_expiry_date - now().date())<timedelta(days=15):
                vehicle.PUC_expired=True
        else:
            vehicle.PUC_expired=False
        
        vehicle.save()

def check_expiry_insurance():
    vehicles = Vehicle.objects.all()
   
    for vehicle in vehicles:
        if(vehicle.Notifications):
            if (vehicle.Insurance_expiry_date - now().date())<timedelta(days=15):
                vehicle.Insurance_expired=True
        else:
            vehicle.Insurance_expired=False
        vehicle.save()

def check_expiry_license():
    drivers = Driver.objects.all()
    for driver in drivers:
        if (driver.License_expiry - now().date())<timedelta(days=15):
            driver.License_expired=True
        else:
            driver.License_expired=False
        driver.save()