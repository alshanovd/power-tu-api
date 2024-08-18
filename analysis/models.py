from django.db import models

class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255)
    def __str__(self):
        return self.client_id
    
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_id


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_gender = models.CharField(max_length=10)
    user_country = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    def __str__(self):
        return self.order_id
    
class OrderedItems(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.id
