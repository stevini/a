from django.db import models
from django.contrib.auth.models import User

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

    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(null=False, default=True)
    order_amount = models.IntegerField(default=0)
    name = models.CharField(max_length=200, unique=True)
    code = models.IntegerField(unique=True, null=True, blank=True)
    sellp = models.FloatField(null=True)
    buyp = models.FloatField(null=True)
    quantity_in_stock = models.IntegerField(default=0,)
    image = models.ImageField(upload_to='web/static/assets/images/demos/demo-13/products/', null=True, blank=True)

    def get_total(self):
        total = self.order_amount * self.sellp
        return total

class Category(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(null=True)
    product = models.ManyToManyField(Products)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Products)
    order_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.total} by {self.user.username}"

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Products)

    def __str__(self):
        return f"{self.product} by "

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Products)
    checkout_time = models.DateTimeField(auto_now_add=True)