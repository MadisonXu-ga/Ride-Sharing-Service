from django.contrib import admin
from .models import RideUser, Driver, Ride, RideSharer

# Register your models here.
admin.site.register(RideUser)
admin.site.register(Driver)
admin.site.register(Ride)
admin.site.register(RideSharer)