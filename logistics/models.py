from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db import models
import datetime
from django.core.validators import MinLengthValidator,MinValueValidator
from django.forms.widgets import Widget

# Create your models here.

def date_validate(date):
    if(date<=datetime.date.today()):
        raise ValidationError("The date cannot be in the past!")

class Driver(models.Model):
    Name = models.CharField(max_length=14, verbose_name="Driver's Name")
    License_number = models.CharField(verbose_name="DL Number", unique=True, max_length=15, validators=[MinLengthValidator(15,message = "Invalid License Number")])
    License_expiry = models.DateField(verbose_name="License Expiry", validators=[date_validate])#,input_formats = ['%d/%m/%Y'])
    Contact_number = models.CharField(verbose_name="Contact Number", max_length=10,validators=[MinLengthValidator(10,message = "Invalid Contact Number")])

    def __str__(self):
        return self.Name

TYPE_CHOICES = (
    ('PICKUP','PICKUP'),
    ('19FT','19FT'),
    ('22FT','22FT'),
    ('32FT S','32FT S'),
    ('32FT M','32FT M'),
    ('OTHER','OTHER'),
)

class Vehicle(models.Model):
    Owner  = models.CharField(max_length=14, verbose_name="Owner's Name")
    ##format GJ11BCXXXX
    RC_number = models.CharField(verbose_name="RC Number",max_length=13, validators=[MinLengthValidator(12,message = "Invalid RC Number")])
    PAN_number = models.CharField(verbose_name="PAN Number", max_length=10, validators=[MinLengthValidator(10,message = "Invalid PAN Number")])
    
    Type = models.CharField(verbose_name="Type of Vehicle", choices=TYPE_CHOICES, default='PICKUP',max_length=10)
    Other = models.CharField(default=None,verbose_name='',max_length=10)
    Insurance_policy_number = models.CharField(max_length=14, null = False)
    Insurance_expiry_date = models.DateField(null=False,validators=[date_validate])#,input_formats = ['%d/%m/%Y'])
    Safety_equipments = models.BooleanField(default=False)
    GPS = models.BooleanField(default=False)
    Contact_number = models.CharField(max_length=10,validators=[MinLengthValidator(10,message = "Invalid Contact Number")])
    

    def __str__(self):
        return self.RC_number

class Trip_detail(models.Model):
    Vehicle = models.ForeignKey(
        'Vehicle',
         on_delete=models.RESTRICT,
         verbose_name="RC Number",
         )
    Driver = models.ForeignKey(
        'Driver',
        verbose_name="Driver's Name",
        on_delete=models.RESTRICT,
    )
    Trip_id = models.CharField(max_length=14)
    Source = models.CharField(max_length=14)
    # Destination (can be multiple)
    Total_payment = models.IntegerField(validators=[MinValueValidator(0)])
    Advance_payment = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.Trip_id

class Bank_detail(models.Model):
    Vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.RESTRICT,
        verbose_name="RC Number",
    )
    Account_number = models.CharField(verbose_name="Account Number",max_length=20)
    Account_holder = models.CharField(verbose_name="Account Holder",max_length=20)
    IFSC = models.CharField(verbose_name="IFSC Code",max_length=20)
    Account_type =models.CharField(verbose_name="Account Type", choices=(('SAVINGS','SAVINGS'),('CURRENT','CURRENT'),), default='CURRENT',max_length=7)
    
    def __str__(self):
        return self.Account_number