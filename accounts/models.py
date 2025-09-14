from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
        ('P', 'Prefer not to say'),
    ]

    email = models.EmailField(unique=True)

    date_of_birth = models.DateField(null=True, 
                                     blank=True, 
                                     help_text="User's date of birth.")
    
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              null=True,
                              blank=True,
                              help_text="User's gender")
    
    height_cm = models.FloatField(null=True,
                                  blank=True,
                                  help_text="Current height in centimeters")
    
    weight_kg = models.FloatField(null=True,
                                  blank=True,
                                  help_text="Current weight in kilograms")
    
    def __str__(self):
        return self.username