from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15, unique=True)  
    my_location_link = models.URLField(blank=True, null=True) 
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)  # 

    def __str__(self):
        return self.username
