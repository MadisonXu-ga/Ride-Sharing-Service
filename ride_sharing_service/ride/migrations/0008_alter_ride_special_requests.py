# Generated by Django 4.1.5 on 2023-02-05 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0007_alter_ride_sharer_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='special_requests',
            field=models.TextField(blank=True, null=True),
        ),
    ]
