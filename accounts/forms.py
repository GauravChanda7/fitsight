from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from datetime import date
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'height_cm', 'weight_kg')

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'height_cm', 'weight_kg')
        widgets = {
            'date_of_birth' : forms.DateInput(attrs={'type' : 'date'})
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 13:
                raise ValidationError("You must be older than 13 years")
        
        return dob
    
    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height_cm')
        weight = cleaned_data.get('weight_kg')

        if height is not None and height <= 0:
            self.add_error('height_cm', 'Height must be a positive number')

        if weight is not None and weight <= 0:
            self.add_error('weight_kg', 'Weight must be a positive number')

        return cleaned_data