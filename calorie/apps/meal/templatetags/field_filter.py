from django.template import Library

from calorie.apps.meal.models import Food

register = Library()


@register.simple_tag
def get_field_meal(user, field):
    foods = Food.objects.raw(
        f'SELECT "meal_food"."id" ,"meal_food"."{field}" FROM "meal_food" INNER JOIN "meal_meal"  ON ("meal_food"."meal_id" = "meal_meal"."id") WHERE "meal_meal"."user_id" = "{user.id}"'
    )
    total = 0
    for food in foods:
        total += getattr(food, field)
    return total
