from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['orders__created_at']


class DeliveryAddress(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=20)
    apartment = models.IntegerField(blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Delivery addresses'

    def __str__(self):
        return f'City: {self.city}, street: {self.street}'


class Driver(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    vehicle_code = models.IntegerField(unique=True)
    vehicle_name = models.CharField(max_length=50)
    vehicle_max_weight = models.IntegerField()
    vehicle_max_volume = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.vehicle_name}'


class Manager(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField()


    def __str__(self):
        return self.name


class OrderInfo(models.Model):

    STATUS_CHOICES = [
        ('confirmed', 'Підтверджено'),
        ('on_the_way', 'В дорозі'),
        ('delivered', 'Доставлено'),
        ('canceled', 'Відмінено')
    ]

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='orders')
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='manager')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='driver')
    order_number = models.IntegerField(unique=True)
    order_weight = models.IntegerField()
    order_volume = models.DecimalField(max_digits=5, decimal_places=2)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_adress = models.CharField(max_length=50)
    unload_service = models.BooleanField(default=False)
    manipulator_service = models.BooleanField(default=False)
    additional_info = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField()
    ship_date = models.DateField()
    ship_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    class Meta:
        verbose_name_plural = 'Orders info'

    def __str__(self):
        return f'{self.order_number} {self.client.name} {self.manager.name} {self.driver.name}'
