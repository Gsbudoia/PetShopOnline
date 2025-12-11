import datetime
from django.db import models
from core.models import Pet
from django.conf import settings
from django.core.exceptions import ValidationError

class ServiceType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Serviço")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # NOVO CAMPO: Duração em minutos (ex: 30, 60)
    duration = models.IntegerField(verbose_name="Duração (minutos)", default=30)

    def __str__(self):
        return f"{self.name} ({self.duration} min)"

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    # Mudei de ManyToMany para ForeignKey para simplificar a lógica inicial (1 serviço por vez)
    # Se quiser combos (Banho + Tosa), crie um ServiceType chamado "Banho Completo"
    service = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True) 
    
    date = models.DateTimeField(verbose_name="Data e Hora")
    notes = models.TextField(blank=True, verbose_name="Observações")
    vet = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.pet.name} - {self.date}"

    # Lógica de validação (Não deixa salvar se tiver conflito)
    def clean(self):
        if not self.service:
            return

        # Calcula a hora que termina esse agendamento
        start_time = self.date
        end_time = start_time + datetime.timedelta(minutes=self.service.duration)

        # Procura agendamentos que colidem com esse horário
        conflicts = Appointment.objects.filter(
            date__lt=end_time,           # Começa antes deste terminar
            date__gt=start_time - datetime.timedelta(minutes=120) # Otimização de busca
        ).exclude(id=self.id) # Não conta ele mesmo se for edição

        for appointment in conflicts:
            # Calcula o fim do agendamento existente
            existing_end = appointment.date + datetime.timedelta(minutes=appointment.service.duration)
            
            # Verifica sobreposição real
            if (start_time < existing_end) and (end_time > appointment.date):
                raise ValidationError(f"Horário indisponível. Já existe um agendamento entre {appointment.date.strftime('%H:%M')} e {existing_end.strftime('%H:%M')}.")