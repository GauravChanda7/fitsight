from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

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
    

class WeightEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weight_history")
    weight_kg = models.FloatField()
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Weight Entries"
    
    def __str__(self):
        return f"{self.user.username} - {self.weight_kg}kg in {self.date}"
