from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment, ServiceType
from core.models import Customer

@login_required
def schedule_service(request):
    # ... (mantenha o código que já fizemos aqui) ...
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

# --- ADICIONE ESTA FUNÇÃO NOVA ABAIXO ---
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