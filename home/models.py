from django.db import models
#new
from django.contrib.auth.models import User



# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122) 
    email = models.EmailField()
    message = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.name
    
    
#new
class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=122) 
    phone_number= models.CharField(max_length=15)
    email = models.EmailField(blank=True,null =True)
    
    def __str__(self):
        return f"{self.name} ({self.phone_number})"