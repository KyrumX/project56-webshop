from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import  post_save
from django.dispatch import receiver
import datetime

# Create your models here.

class Customers(models.Model):
    class Meta:
        verbose_name_plural = "Customers"

    customerID = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    telephone = models.CharField(max_length=12)
    isRegistered = models.BooleanField()
    isBlocked = models.BooleanField(default=False)

class Address(models.Model):
    class Meta:
        verbose_name_plural = "Customer addresses"
        unique_together = ('customerID', 'address')

    customerID = models.ForeignKey(Customers, db_column='customerID', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=25)
    postalcode = models.CharField(max_length=10)

class Products(models.Model):
    class Meta:
        verbose_name_plural = "Products"

    prodNum = models.IntegerField(primary_key=True)
    prodName = models.CharField(max_length=200)
    prodPrice = models.DecimalField(max_digits=5, decimal_places=2)
    prodStock = models.IntegerField()

    def __str__(self):
        return (str(self.prodNum))

class ProductDetails(models.Model):
    class Meta:
        verbose_name_plural = "Product details"

    prodNum = models.ForeignKey(Products, db_column='prodNum', on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default="Comic")
    publisher = models.CharField(max_length=50)
    totalPages = models.IntegerField()
    language = models.CharField(max_length=25, default="Engels")
    rating = models.IntegerField()
    author = models.CharField(max_length=50)
    desc = models.TextField()
    imageLink = models.CharField(max_length=300)
    pubDatum = models.CharField(max_length=30, default="1 januari, 1990")

    def __str__(self):
        return (str(self.prodNum))

class WishList(models.Model):
    class Meta:
        unique_together = ('custId', 'productNum')

    custId = models.ForeignKey(Customers, db_column='custId', on_delete=models.CASCADE)
    productNum = models.ForeignKey(Products, db_column='productNum', on_delete=models.CASCADE)

class Orders(models.Model):
    class Meta:
        verbose_name_plural = "Orders"

    orderNum = models.IntegerField(primary_key=True)
    customerID = models.ForeignKey(Customers, db_column='customerID', on_delete=models.CASCADE)
    orderDate = models.DateField()
    orderStatus = models.CharField(max_length=15)

    def __str__(self):
        return (str(self.orderNum))

class OrderDetails(models.Model):
    class Meta:
        unique_together = ('orderNum', 'productNum')
        verbose_name_plural = "Order details"

    orderNum = models.ForeignKey(Orders, db_column='orderNum', on_delete=models.CASCADE)
    productNum = models.ForeignKey(Products, db_column='productNum', on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return (str(self.orderNum))

class ShoppingCart(models.Model):
    session_key = models.CharField(max_length=40)
    prodNum = models.ForeignKey(Products, db_column='prodNum', on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        unique_together = ('session_key', 'prodNum')

class UserVisits(models.Model):
    class Meta:
        verbose_name_plural = "User Visits"
    customerID = models.IntegerField(default=0)
    is_staff = models.BooleanField()
    visits = models.IntegerField()

class Dates(models.Model):
    class Meta:
        verbose_name_plural = "Dates"
    customerID = models.ForeignKey(UserVisits, db_column='customerID', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)

class Reviews(models.Model):
    class Meta:
        verbose_name_plural = "Product Reviews"
        unique_together = ('prodNum', 'customerID')
    customerID = models.ForeignKey(Customers, db_column='customerID', on_delete=models.CASCADE)
    prodNum = models.ForeignKey(Products, db_column='productNum', on_delete=models.CASCADE)
    review = models.CharField(max_length=1500)
    rating = models.IntegerField()
    date = models.DateField(default=datetime.date.today)
