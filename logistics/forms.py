# import form class from django
from django import forms
from django.forms import widgets 

#import models from models.py
from .models import Trip_detail,Vehicle,Driver,Bank_detail


class Trip_detailForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Trip_detail
        # fields = "__all__"
        exclude = ['Date']


class VehicleForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Vehicle
        fields = "__all__"
        widgets = {
            'RC_number': widgets.TextInput(attrs={'placeholder':'GJ-XX-AB-XXXX',}),
            'Contact_number': widgets.TextInput(attrs={'placeholder':'1234567890',}),
            'Insurance_expiry_date': widgets.DateInput( format='%d-%m-%y', attrs={'type':'date', 'placeholder':'DD-MM-YYYY'}),
            'PUC_expiry_date': widgets.DateInput( format='%d-%m-%y', attrs={'type':'date', 'placeholder':'DD-MM-YYYY'}),
        }

class DriverForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Driver
        fields = "__all__"
        widgets = {
            'License_expiry' : widgets.DateInput(format='%d-%m-%Y', attrs={'type':'date', 'placeholder':'DD-MM-YYYY'}),
        }

class Bank_detailForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Bank_detail
        fields = "__all__"