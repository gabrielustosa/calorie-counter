from django.urls import path

from . import views

app_name = 'calorie'

urlpatterns = [
    path('', views.HomeCalorieView.as_view(), name='home')
]
