import os
from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BrandModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['manufacturer', 'name'], name='unique_brand_model')
        ]


class Car(models.Model):
    PETROL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('Coupe', 'Coupe'),
        ('Convertible', 'Convertible'),
        ('Hatchback', 'Hatchback'),
        ('Van', 'Van'),
        ('Wagon', 'Wagon'),
    ]

    GEAR_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]

    model_name = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    petrol_type = models.CharField(
        max_length=10, choices=PETROL_CHOICES, default='Petrol')
    car_type = models.CharField(
        max_length=12, choices=CAR_TYPE_CHOICES, default='Sedan')
    gear_type = models.CharField(
        max_length=10, choices=GEAR_CHOICES, default='Manual')
    created_at = models.DateTimeField(auto_now_add=True)
    milage = models.IntegerField(default=0)

    def get_price(self):
        return format_swedish_currency(self.price)

    def get_milage(self):
        return f'{self.milage} km'

    def __str__(self):
        return f"{self.model_name} ({self.year})"


def car_images_upload_to(instance, filename):
    return os.path.join('car_images', str(instance.car.id) + '_' + filename)


class CarImages(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=car_images_upload_to)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.featured:
            CarImages.objects.filter(
                car=self.car, featured=True).update(featured=False)
        super(CarImages, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.car.model_name.name} | image | {self.featured}'


class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.car} by {self.user} on {self.reservation_date}"

def format_swedish_currency(amount):
    amount = round(amount, 2)
    formatted_amount = f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted_amount} kr"