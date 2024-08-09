from django.db import models


# Create your models here.

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.product_id


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_gender = models.CharField(max_length=10)
    user_country = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.order_id
    
class OrderedItems(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.id


