from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class DefaultImages(models.Model):

    def __str__(self):
        return self.name

    def img(self):
        return self.image

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='default_images/')


class Products(models.Model):
    def __str__(self):
        return self.name

    active = models.BooleanField(null=False, default=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    buyp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    code = models.IntegerField(unique=True, null=True, blank=True)
    order_amount = models.PositiveIntegerField(default=0,)
    name = models.CharField(max_length=200, unique=True)
    sellp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='web/static/assets/images/demos/demo-13/products/', null=True, blank=True)

    @property
    def get_total(self):
        total = self.sellp * self.order_amount
        return total


class Category(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(null=True)
    product = models.ManyToManyField(Products)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    avatar = models.ImageField(upload_to='web/static/assets/images/demos/demo-13/avatars/', blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, region='KE', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Products)
    order_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user}-{self.pk}-{self.order_time.time()}".capitalize()
    
    def subtotals(self):
        products = set()
        for item in self.product.all():
            products.add(item.get_total)
        return sum(products)

    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Products)

    def __str__(self):
        return f"{self.product} by "

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Products)
    checkout_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user}-{self.pk}-{self.checkout_time.time()}".capitalize()
    

    def subtotals(self):
        products = set()
        for item in self.product.all():
            products.add(item.get_total)
        return sum(products)


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    product = models.ManyToManyField(Products)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number using uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def subtotals(self):
        products = set()
        for item in self.product.all():
            products.add(item.get_total)
        return sum(products)