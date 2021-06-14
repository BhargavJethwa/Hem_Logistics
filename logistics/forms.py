# import form class from django
from django import forms
from django.forms import widgets 
from searchableselect.widgets import SearchableSelect

#import models from models.py
from .models import Trip_detail,Vehicle,Driver,Bank_detail,Client


class Trip_detailForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Trip_detail
        # fields = "__all__"
        exclude = ['Date_created','Finished','Total_payment','Destination','Other_charges','Load_unload_charges']


class VehicleForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Vehicle
        # fields = "__all__"
        exclude = ['PUC_expired','Insurance_expired','Available']
        widgets = {
            'RC_number': widgets.TextInput(attrs={'placeholder':'GJ-XX-AB-XXXX',}),
            'Contact_number': widgets.TextInput(attrs={'placeholder':'1234567890',}),
            'Insurance_expiry_date': widgets.DateInput( format='%Y-%m-%d', attrs={'type':'date','placeholder':'DD-MM-YYYY'}),
            'PUC_expiry_date': widgets.DateInput( format='%Y-%m-%d', attrs={'type':'date','placeholder':'DD-MM-YYYY'}),
        }

class DriverForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Driver
        # fields = "__all__"
        exclude = ['License_expired']
        widgets = {
            'License_expiry' : widgets.DateInput(format='%Y-%m-%d', attrs={'type':'date', 'placeholder':'DD-MM-YYYY'}),
        }

    # Vehicle = forms.ModelMultipleChoiceField(
    #     queryset=Vehicle.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

class Bank_detailForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Bank_detail
        fields = "__all__"

class ClientForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Client
        fields = "__all__"