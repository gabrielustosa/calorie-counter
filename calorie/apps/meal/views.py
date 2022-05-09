from decimal import Decimal

import requests
from django.contrib import messages

from googletrans import Translator
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView

from calorie.apps.meal.models import Meal, Food

translator = Translator()


class HomeCalorieView(TemplateView):
    template_name = 'calorie/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = Meal.objects.filter(user=self.request.user)

        context['foods'] = get_food_list(self.request.user)
        return context


class ManageMealView(TemplateView):
    template_name = 'meal/manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = Meal.objects.filter(user=self.request.user)
        return context


class CreateMealView(CreateView):
    template_name = 'meal/create.html'
    model = Meal
    fields = ('name', 'time')
    success_url = reverse_lazy('meal:manage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteMealView(DeleteView):
    template_name = 'meal/delete.html'
    model = Meal
    success_url = reverse_lazy('meal:manage')

    def dispatch(self, request, *args, **kwargs):
        meal = Meal.objects.get(pk=self.kwargs.get('pk'))
        if meal:
            if meal.user != request.user:
                raise Http404()
        return super().dispatch(request, *args, **kwargs)


class CreateFoodView(CreateView):
    template_name = 'meal/create_food.html'
    model = Food
    fields = (
        'name',
        'quantity',
        'measure',
    )
    success_url = reverse_lazy('meal:manage')

    def dispatch(self, request, *args, **kwargs):
        meal = Meal.objects.get(pk=self.kwargs.get('pk'))
        if meal:
            if meal.user != request.user:
                raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.instance
        meal = Meal.objects.get(pk=self.kwargs.get('pk'))

        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        translation = translator.translate(instance.name, dest='en').text
        response = requests.get(api_url + translation,
                                headers={'X-Api-Key': 'QSAd5X7UrPUdhSkgsBKOAw==IXdO3mh5I2C1yPDR'})
        if response.status_code == requests.codes.ok:
            json_data = response.json()
            data = json_data.get('items')[0]
            sugar = calculate(100, data['sugar_g'])
            fiber = calculate(100, data['fiber_g'])
            sodium = calculate(100, data['sodium_mg'])
            potassium = calculate(100, data['potassium_mg'])
            fat_saturated = calculate(100, data['fat_saturated_g'])
            fat_total = calculate(100, data['fat_total_g'])
            calories = calculate(100, data['calories'])
            cholesterol = calculate(100, data['cholesterol_mg'])
            protein = calculate(100, data['protein_g'])
            carbohydrates = calculate(100, data['carbohydrates_total_g'])

            if instance.measure == 'G' or instance.measure == 'ML':
                measure = instance.quantity
            else:
                measure = instance.quantity * 1000

            instance.sugar = sugar * measure
            instance.fiber = fiber * measure
            instance.sodium = sodium * measure
            instance.potassium = potassium * measure
            instance.fat_saturated = fat_saturated * measure
            instance.fat_total = fat_total * measure
            instance.calories = calories * measure
            instance.cholesterol = cholesterol * measure
            instance.protein = protein * measure
            instance.carbohydrates_total = carbohydrates * measure
            instance.meal = meal

            user = self.request.user
            user.current_calories = user.current_calories + instance.calories
            user.save()
        else:
            messages.error(self.request, 'Ocorreu um erro ao tentar adicionar a comida.')
            return redirect('meal:manage')

        return super().form_valid(form)


def calculate(n1, n2):
    try:
        z = n2 / n1
        return Decimal(z)
    except ZeroDivisionError:
        return 0


def get_food_list(user):
    fields = ['sugar', 'fiber', 'sodium', 'potassium', 'fat_saturated',
              'fat_total', 'cholesterol', 'protein',
              'carbohydrates_total']

    foods = Food.objects.filter(meal__user=user)
    result = {}
    for f in fields:
        name = Food._meta.get_field(f).verbose_name
        result[name] = 0
    for food in foods:
        for v, k in enumerate(result.keys()):
            result[k] += round(float(getattr(food, fields[v])))
    return result
