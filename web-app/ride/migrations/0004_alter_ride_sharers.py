# Generated by Django 4.1.5 on 2023-02-01 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0003_ride_sharers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='sharers',
            field=models.ManyToManyField(null=True, related_name='shared_rides', to='ride.rideuser'),
        ),
    ]
