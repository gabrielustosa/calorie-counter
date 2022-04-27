from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView

from calorie.apps.meal.models import Meal


class HomeCalorieView(TemplateView):
    template_name = 'calorie/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


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
