from django.contrib import admin

# Register your models here.
from .models import Driver,Vehicle,Trip_detail,Bank_detail,Transaction,Client

admin.site.register(Driver)
admin.site.register(Bank_detail)
admin.site.register(Vehicle)
admin.site.register(Trip_detail)
admin.site.register(Transaction)
admin.site.register(Client)