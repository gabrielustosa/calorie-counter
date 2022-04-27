from django.contrib import admin

from calorie.apps.meal.models import Meal


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
