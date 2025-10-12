from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)       
    category = models.CharField(max_length=100)   #
    image = models.ImageField(upload_to='products/')
    embedding = models.JSONField(blank=True, null=True) 

    def __str__(self):
        return f"{self.name} ({self.category})"
