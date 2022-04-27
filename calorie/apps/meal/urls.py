from django.urls import path

from . import views

app_name = 'meal'

urlpatterns = [
    path('gerenciar/', views.ManageMealView.as_view(), name='manage'),
    path('criar/', views.CreateMealView.as_view(), name='create'),
    path('deletar/<int:pk>/', views.DeleteMealView.as_view(), name='delete'),
    path('comida/adicionar/<int:pk>/', views.CreateFoodView.as_view(), name='create_food'),
]
