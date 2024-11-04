from django.contrib import admin

# Register your models here.
from .models import Brand,OilType,CarForRent,CarForSale,CustomUser
admin.site.register(Brand)
admin.site.register(OilType)
admin.site.register(CarForRent)
admin.site.register(CarForSale)
admin.site.register(CustomUser)