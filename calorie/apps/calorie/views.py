from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomeCalorieView(TemplateView):
    template_name = 'calorie/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
