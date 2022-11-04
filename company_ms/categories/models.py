from django.db import models

#Category model
class Category(models.Model):
    #Basic fields
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    #Utility fields
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
