from django.contrib import admin

# Register your models here.
from .models import Driver,Vehicle,Trip_detail

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Trip_detail)