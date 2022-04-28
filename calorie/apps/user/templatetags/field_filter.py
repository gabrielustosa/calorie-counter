from django.template import Library

from calorie.apps.meal import models

register = Library()


@register.simple_tag
def get_field_meal(user, field):
    meals = models.Meal.objects.filter(user=user)
    total = 0
    for meal in meals.all():
        for food in meal.foods.all():
            if hasattr(food, field):
                total += getattr(food, field)
    return total
