from django.urls import path
from . import views

urlpatterns = [
    # Rota para ver a lista de agendamentos (que estava dando erro)
    path('meus-agendamentos/', views.appointment_list, name='appointment_list'),
    
    # Rota para criar novo agendamento (que criamos antes)
    path('novo/', views.schedule_service, name='schedule_service'),
]