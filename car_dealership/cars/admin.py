from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Manufacturer, BrandModel, Car, CarImages, Reservation


class ManufacturerAdmin(admin.ModelAdmin):
    field = ['__all__']


class BrandModelAdmin(admin.ModelAdmin):
    field = ['__all__']


class CarAdmin(admin.ModelAdmin):
    field = ['__all__']
    
class ImageAdmin(admin.ModelAdmin):
    field = ['__all__']

admin.site.register(CarImages, ImageAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(BrandModel, BrandModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Reservation)