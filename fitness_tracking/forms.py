from .models import WorkoutSession, Set, Exercise
from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.db.models import Q

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['date']
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'}),
        }

class AddExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['muscle_group', 'exercise_name']

    
class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['exercise_name', 'reps', 'weight_kg']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['exercise_name'].queryset = Exercise.objects.filter(Q(user=user))
