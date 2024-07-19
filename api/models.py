from django.db import models

# Create your models here.

class PowerUser(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username