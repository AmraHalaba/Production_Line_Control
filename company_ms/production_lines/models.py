from django.db import models
from profiles.models import *
from products.models import *

# Production line model
class ProductionLine(models.Model):
    #Basic fields
    name        = models.CharField(max_length=120)
    
    #Related fields
    team_leader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products    = models.ManyToManyField(Product)
    
    #Utility fields
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
