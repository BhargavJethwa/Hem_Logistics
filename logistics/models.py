from django.db import models
from django.core.validators import MinLengthValidator,MinValueValidator

# Create your models here.

class Driver(models.Model):
    Name = models.CharField(max_length=14)
    License_number = models.CharField(max_length=14)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    Number = models.CharField(max_length=14)
    Owner  = models.CharField(max_length=14)
    RC_number = models.CharField(max_length=14)
    PAN_number = models.CharField(max_length=10,primary_key=True, validators=[MinLengthValidator(10,message = "Invalid PAN Number")])
    # Bank details = ( can be multiple accounts)
    Capacity = models.FloatField()
    Insurance_policy_number = models.CharField(max_length=14)
    Insurance_expiry_date = models.DateField()
    Safety_equipments = models.BooleanField(default=False)
    GPS = models.BooleanField(default=False)
    Contact_number = models.CharField(max_length=10,validators=[MinLengthValidator(10,message = "Invalid Contact Number")])
    # name = models.CharField(max_length=20)
    # active = BooleanField()
    # date_added = DateTimeField(default=timezone.now)
    # price = FloatField()
    # make = models.ForeignKey(Make)
    
    def __str__(self):
        return self.name

class Trip_detail(models.Model):
    Vehicle = models.ForeignKey(
        'Vehicle',
         on_delete=models.RESTRICT,
         )
    Driver = models.ForeignKey(
        'Driver',
        on_delete=models.RESTRICT,
    )
    Trip_id = models.CharField(max_length=14,primary_key=True)
    Source = models.CharField(max_length=14)
    # Destination (can be multiple)
    Total_payment = models.IntegerField(validators=[MinValueValidator(0)])
    Advance_payment = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name
