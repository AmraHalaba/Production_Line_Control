from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    bio         = models.TextField()
    profile_pic = models.ImageField(blank=True)
    website     = models.CharField(max_length=220, blank=True)
    
    # Utility Fields
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{}".format(self.user)