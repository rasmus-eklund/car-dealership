# Generated by Django 5.0.6 on 2024-05-28 12:08

import cars.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_alter_carimages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carimages',
            name='image',
            field=models.ImageField(upload_to=cars.models.car_images_upload_to),
        ),
    ]
