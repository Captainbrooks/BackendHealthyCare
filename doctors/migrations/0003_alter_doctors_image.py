# Generated by Django 5.2.1 on 2025-06-12 01:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_timeslot_is_booked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
