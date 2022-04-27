from django.db import models
from calorie.apps.user.models import User


class Meal(models.Model):
    name = models.CharField('Nome', max_length=50)
    time = models.TimeField('Horário')
    user = models.ForeignKey(User, related_name='meals', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField('Nome', max_length=100)
    quantity = models.PositiveIntegerField('Quantidade')
    measure = models.CharField('Medida', max_length=2, choices=[
        ('G', 'Gramas'),
        ('L', 'Litros'),
        ('ML', 'Mili Litros'),
    ])
    sugar = models.DecimalField(max_digits=6, decimal_places=1)
    fiber = models.DecimalField(max_digits=6, decimal_places=1)
    sodium = models.PositiveIntegerField()
    potassium = models.PositiveIntegerField()
    fat_saturated = models.DecimalField(max_digits=6, decimal_places=1)
    fat_total = models.DecimalField(max_digits=6, decimal_places=1)
    calories = models.PositiveIntegerField()
    cholesterol = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=6, decimal_places=1)
    carbohydrates_total = models.DecimalField(max_digits=20, decimal_places=1)
    meal = models.ForeignKey(Meal, related_name='foods', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
