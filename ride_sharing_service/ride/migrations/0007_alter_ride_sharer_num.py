# Generated by Django 4.1.5 on 2023-02-03 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0006_ride_sharer_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='sharer_num',
            field=models.JSONField(default={}),
        ),
    ]
