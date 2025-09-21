from django.contrib import admin
from .models import WorkoutSession, Exercise, Set

# Register your models here.
admin.site.register(WorkoutSession)
admin.site.register(Exercise)
admin.site.register(Set)