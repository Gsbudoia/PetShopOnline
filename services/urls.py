from django.urls import path
from . import views

urlpatterns = [
    # Rota para ver a lista de agendamentos
    path('meus-agendamentos/', views.appointment_list, name='appointment_list'),
    
    # Rota para criar novo agendamento
    path('novo/', views.schedule_service, name='schedule_service'),

    path('gestao/agenda/', views.admin_appointment_list, name='admin_appointment_list'),
    path('gestao/agenda/cancelar/<int:pk>/', views.admin_appointment_delete, name='admin_appointment_delete'),
]