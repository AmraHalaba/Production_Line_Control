from django.db import models

# Product model
class Product(models.Model):
    #Basic fields
    name       = models.CharField(max_length=220)
    short_code = models.CharField(max_length=20)
    descripton = models.TextField(blank=True, null=True)
    
    #Utility fields
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
