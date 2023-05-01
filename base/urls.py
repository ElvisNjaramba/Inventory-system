from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('per_product/<int:pk>', views.per_product, name='per_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('dashboard/', views.dashboard, name='dashboard')
]