from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Vehiculo

admin.site.register(Permission)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    pass
    