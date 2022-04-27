from django.contrib import admin

from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'height',
        'weight',
        'birthday',
        'max_calories',
        'current_calories',
        'sex',
        'is_staff',
    )
