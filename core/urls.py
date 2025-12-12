from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='home'),
    path('novo/', views.customer_add, name='customer_add'),
    path('meus-pets/', views.my_pets, name='my_pets'),
    path('meus-pets/adicionar/', views.cadastrar_pet, name='cadastrar_pet'),
]