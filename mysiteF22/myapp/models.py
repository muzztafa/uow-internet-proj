from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, null=False, default='Windsor')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        total = self.stock + 100
        self.stock = total


class Client(User):
    PROVINCE_CHOICES = [
         ('AB', 'Alberta'),
         ('MB', 'Manitoba'),
         ('ON', 'Ontario'),
         ('QC', 'Quebec'), ]
    company = models.CharField(max_length=50, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES,
                                 default='ON')
    interested_in = models.ManyToManyField(Category)
    photo = models.ImageField(upload_to="uploads/",blank=True)


class Order(models.Model):

    ORDER_VALUES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered')
    ]

    product = models.ForeignKey(Product, related_name='products_ordered', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=0)
    order_status = models.IntegerField(choices=ORDER_VALUES, default=1)
    status_date = models.DateField(default=datetime.now())

    def __str__(self):
        return f"{self.client} - {self.product} - {self.status_date}"

    def total_cost(self):
        product = self.num_units * self.product.price
        return product
