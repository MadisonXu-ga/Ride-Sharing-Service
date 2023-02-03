from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class RideUser(models.Model):
    # user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()

class Driver(models.Model):
    # driver_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(RideUser, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=255)
    license_plate_number = models.CharField(max_length=255)
    max_num_pax = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    special_info = models.TextField(null=True)

class Ride(models.Model):
    owner = models.ForeignKey(RideUser, on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)
    arrival_time = models.DateTimeField()
    vehicle_type = models.CharField(max_length=255)
    num_pax_owner = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    num_pax_total = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    special_requests = models.TextField(null=True)
    is_sharable = models.BooleanField()
    STATUS_CHOICES = (
        (0, 'Open'),
        (1, 'Confirmed'),
        (2, 'Complete'),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='open')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    sharers = models.ManyToManyField(RideUser, related_name='shared_rides', null=True)
    sharer_num = models.JSONField(default={})


class RideSharer(models.Model):
    sharer = models.ForeignKey(RideUser, on_delete=models.CASCADE)
    ride_info = models.ForeignKey(Ride, on_delete=models.CASCADE)