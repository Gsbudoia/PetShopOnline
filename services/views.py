from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment, ServiceType
from core.models import Customer
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def schedule_service(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Agendamento realizado!')
                return redirect('appointment_list') # Redireciona para a lista
            except Exception as e:
                messages.error(request, f'Erro: {e}')
    else:
        form = AppointmentForm(user=request.user)
    return render(request, 'services/schedule.html', {'form': form})

@login_required
def appointment_list(request):
    # Tenta pegar os agendamentos apenas dos pets deste dono
    try:
        customer = request.user.customer
        # Filtra agendamentos onde o pet pertence ao cliente logado
        appointments = Appointment.objects.filter(pet__owner=customer).order_by('date')
    except Customer.DoesNotExist:
        appointments = []
    
    return render(request, 'services/appointment_list.html', {'appointments': appointments})

@staff_member_required
def admin_appointment_list(request):
    # Pega TODOS os agendamentos, ordenados por data
    appointments = Appointment.objects.all().order_by('-date')
    return render(request, 'services/admin_appointment_list.html', {'appointments': appointments})

@staff_member_required
def admin_appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Agendamento cancelado pelo administrador.")
        return redirect('admin_appointment_list')
    return render(request, 'services/confirm_delete.html', {'appointment': appointment})