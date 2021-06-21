from django.db.models.fields import DateField
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db import models
import datetime
from django.core.validators import MinLengthValidator,MinValueValidator, RegexValidator

# Create your models here.

def date_validate(date):
    if(date<=datetime.date.today()):
        raise ValidationError("The date cannot be in the past!")

TYPE_CHOICES = (
    ('PICKUP','PICKUP'),
    ('19FT','19FT'),
    ('22FT','22FT'),
    ('32FT S','32FT S'),
    ('32FT M','32FT M'),
    ('OTHER','OTHER'),
)

class Vehicle(models.Model):
    Owner  = models.CharField(max_length=50, verbose_name="Owner's Name")
    ##format GJ-11-BH-1999
    RC_number = models.CharField(unique =True, verbose_name="RC Number", max_length=13, validators=[MinLengthValidator(12,message = "Invalid RC Number"), RegexValidator('([A-Z]{2})+-([0-9]{1})+-[A-Z]+-[0-9]{4}',message = "Use proper formatting")])
    PAN_number = models.CharField(verbose_name="PAN Number", max_length=10, validators=[MinLengthValidator(10,message = "Invalid PAN Number")])
    
    Type = models.CharField(verbose_name="Type of Vehicle", choices=TYPE_CHOICES, max_length=10)
    Other = models.CharField(blank = True,verbose_name='',max_length=10)
    Insurance_policy_number = models.CharField(max_length=25)
    PUC_expiry_date = models.DateField()
    Insurance_expiry_date = models.DateField(validators=[date_validate])#,input_formats = ['%d/%m/%Y'])
    Safety_equipments = models.BooleanField(default=False)
    GPS = models.BooleanField(default=False)
    Contact_number = models.CharField(max_length=10,validators=[MinLengthValidator(10,message = "Invalid Contact Number"),RegexValidator('([0-9]{10})',message="Should be numeric values only")])
    Notifications = models.BooleanField(verbose_name="Notifications Needed", default=True)
    Insurance_expired = models.BooleanField(default=False)
    PUC_expired = models.BooleanField(default=False)
    Available = models.BooleanField(default=True)
    Balance = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if(self.Other):
            self.Other = self.Other.upper()
        self.Owner = self.Owner.upper()
        super(Vehicle, self).save(*args, **kwargs)

    def __str__(self):
        return self.RC_number

class Driver(models.Model):
    Name = models.CharField(max_length=50)
    License_number = models.CharField(verbose_name="DL Number", unique=True, max_length=15, validators=[MinLengthValidator(15,message = "Invalid License Number")])
    License_expiry = models.DateField(verbose_name="License Expiry", validators=[date_validate])#,input_formats = ['%d/%m/%Y'])
    Contact_number = models.CharField(verbose_name="Contact Number", max_length=10,validators=[RegexValidator('[0-9]{10}',message = "Invalid Number")])
    Vehicle=models.ManyToManyField(Vehicle)
    License_expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.Name = self.Name.upper()
        super(Driver, self).save(*args, **kwargs)

    def __str__(self):
        return self.Name

class Client(models.Model):
    Name = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

class Trip_detail(models.Model):
    Client = models.ForeignKey(
        'Client',
        verbose_name="Client's Name",
        on_delete=models.RESTRICT,
    )
    Driver = models.ForeignKey(
        'Driver',
        verbose_name="Driver's Name",
        on_delete=models.RESTRICT,
    )
    Vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.RESTRICT,
        verbose_name="RC Number",
    )
    Bank_detail = models.ForeignKey(
        'Bank_detail',
        on_delete=models.RESTRICT,
        verbose_name="Bank Details",
    )
    Trip_id = models.CharField(max_length=50)
    Total_payment = models.IntegerField(validators=[MinValueValidator(0)])
    Rate_type = models.CharField(verbose_name="Rate Type", choices=(('FIX','FIX'),('VARIABLE','VARIABLE'),),max_length=8)
    Distance = models.IntegerField(verbose_name="Distance (Kms)",validators=[MinValueValidator(0)])
    Rate = models.IntegerField(default=8,validators=[MinValueValidator(0)], blank=True)
    Freight = models.IntegerField(validators=[MinValueValidator(0)])
    Advance_payment = models.IntegerField(validators=[MinValueValidator(0)])
    Date_created=models.DateField(auto_now_add=True)
    Source = models.CharField(max_length=50)
    Destination = models.TextField()
    Load_unload_charges = models.TextField()
    Other_charges = models.TextField()
    Finished=models.BooleanField(default=False)

    def __str__(self):
        return self.Trip_id

class Bank_detail(models.Model):
    Vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.RESTRICT,
        verbose_name="RC Number",
    )
    Account_number = models.CharField(verbose_name="Account Number",max_length=20)
    Account_holder = models.CharField(verbose_name="Account Holder",max_length=50)
    IFSC = models.CharField(verbose_name="IFSC Code",max_length=20)
    Account_type = models.CharField(verbose_name="Account Type", choices=(('SAVINGS','SAVINGS'),('CURRENT','CURRENT'),),max_length=7)
    
    def __str__(self):
        return self.Account_number
        
class Transaction(models.Model):
    Trip_detail = models.ForeignKey(
        'Trip_detail',
        on_delete=models.RESTRICT,
        verbose_name="Trip",
        blank=True,
        null=True,
    )
    Vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.RESTRICT,
        verbose_name="RC Number",
    )
    
    Bank_detail = models.ForeignKey(
        'Bank_detail',
        on_delete=models.RESTRICT,
        verbose_name="Bank Detail",
    )

    Date_created = models.DateField(default=now)
    Amount = models.IntegerField()
    Details = models.CharField(max_length=50,verbose_name="Detail")
    Is_advance = models.BooleanField(default=False)
    
    def __str__(self):
        return self.id
        