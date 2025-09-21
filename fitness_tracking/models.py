from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, Count, F

# Create your models here.


class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s workout on {self.date}"
    
    def total_weight_lifted(self):
        return Set.objects.filter(session = self).aggregate(
            total_volume = Sum(F('weight_kg') * F('reps'))
            )['total_volume'] or 0
    
    def target_muscles(self):
        return Set.objects.filter(session = self).values_list('exercise_name__muscle_group', flat=True).distinct()

class Exercise(models.Model):
    MUSCLE_GROUP_CHOICES = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('legs', 'Legs'),
        ('biceps', 'Biceps'),
        ('triceps', 'Triceps'),
        ('shoulders', 'Shoulders'),
        ('core', 'Core'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUP_CHOICES)

    class Meta:
        ordering = ['muscle_group', 'exercise_name']
        unique_together = ('user', 'exercise_name')

    def __str__(self):
        return f"{self.get_muscle_group_display()} - {self.exercise_name}"
    
class Set(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    exercise_name = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.PositiveSmallIntegerField()
    weight_kg = models.FloatField()

    def __str__(self):
        return f"{self.reps} of {self.exercise_name} at {self.weight_kg}kg"
