from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    ]

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Data', {
            'fields' : ('date_of_birth', 'gender', 'height_cm', 'weight_kg')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields' : ('date_of_birth', 'gender', 'height_cm', 'weight_kg')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)