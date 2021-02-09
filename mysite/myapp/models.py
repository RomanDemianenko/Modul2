from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


# Create your models here.
from django.utils import timezone


class MyUser(AbstractUser):
    cash = models.DecimalField(decimal_places=5, max_digits=15, default=10000)

# class Customer(models.Model):
#     user = models.ForeignKey(MyUser, related_name='costumer', on_delete=models.CASCADE)
#     name = models.CharField(max_length=20)
#     email = models.EmailField(unique=True)
#
#
#     def __str__(self):
#         return "Покупатель: {}".format(self.user)


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=30, null=True)
    slug = models.SlugField(blank=True, null=True)
    price = models.DecimalField(decimal_places=5, max_digits=15)
    image = models.ImageField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}: quantity-{self.quantity}'


class Order(models.Model):
    costumer = models.ForeignKey(MyUser, related_name='costumer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(decimal_places=5, max_digits=15)
    order_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.product} was bought by {self.costumer} at {self.order_time}'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Cancel(models.Model):
    come_back = models.ForeignKey(Order, related_name='come_back', on_delete=models.CASCADE)
    cancel_date = models.DateTimeField(auto_now=True)
