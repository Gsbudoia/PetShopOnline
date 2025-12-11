from django import forms
from django.utils import timezone
from .models import Appointment
from core.models import Customer, Pet
import datetime

# Definindo os horários fixos do seu Petshop
HORARIOS_DISPONIVEIS = [
    ('09:00', '09:00'),
    ('09:30', '09:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('13:00', '13:00'), # Pausa pro almoço
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
    ('17:00', '17:00'),
    ('17:30', '17:30'),
]

class AppointmentForm(forms.ModelForm):
    # Campos "Virtuais" (Não existem no banco, usamos só pro formulário)
    escolha_data = forms.DateField(
        label="Data do Agendamento",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    escolha_hora = forms.ChoiceField(
        label="Horário",
        choices=HORARIOS_DISPONIVEIS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Appointment
        # Note que removemos o campo 'date' original daqui, pois vamos construí-lo manualmente
        fields = ['pet', 'service', 'notes'] 
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'pet': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 1. Filtra os pets do usuário
        if user:
            try:
                customer = user.customer
                self.fields['pet'].queryset = Pet.objects.filter(owner=customer)
            except Customer.DoesNotExist:
                self.fields['pet'].queryset = Pet.objects.none()

        # 2. Bloqueia datas passadas no HTML (Visual)
        hoje = timezone.now().date()
        self.fields['escolha_data'].widget.attrs['min'] = hoje

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('escolha_data')
        hora_str = cleaned_data.get('escolha_hora')
        service = cleaned_data.get('service')

        if not data or not hora_str or not service:
            return # Se faltar campo, o Django já mostra erro nativo

        # --- VALIDAÇÃO 1: NÃO PODE SER PASSADO ---
        # Converte a string de hora '09:00' para números
        hora, minuto = map(int, hora_str.split(':'))
        
        # Cria o objeto datetime completo
        data_hora_agendamento = datetime.datetime.combine(data, datetime.time(hora, minuto))
        
        # Torna a data "consciente" de fuso horário (importante pro Django não dar erro)
        if timezone.is_naive(data_hora_agendamento):
            data_hora_agendamento = timezone.make_aware(data_hora_agendamento)

        if data_hora_agendamento < timezone.now():
            raise forms.ValidationError("Você não pode agendar para uma data ou hora que já passou.")

        # --- VALIDAÇÃO 2: CONFLITO DE HORÁRIO ---
        # Calculamos quando acaba esse serviço
        fim_servico = data_hora_agendamento + datetime.timedelta(minutes=service.duration)

        # Procura conflitos no banco
        conflitos = Appointment.objects.filter(
            date__lt=fim_servico,
            date__gt=data_hora_agendamento - datetime.timedelta(minutes=120) 
            # Dica: Otimização para não buscar no banco inteiro, busca só perto do horário
        )

        for agendamento in conflitos:
            # Calcula o fim do agendamento que JÁ existe no banco
            fim_existente = agendamento.date + datetime.timedelta(minutes=agendamento.service.duration)
            
            # Se o horário se sobrepõe
            if (data_hora_agendamento < fim_existente) and (fim_servico > agendamento.date):
                raise forms.ValidationError(f"Desculpe, o horário das {hora_str} já está ocupado por outro pet.")

        # Se passou por tudo, salvamos a data completa no formulário para usar no save()
        self.cleaned_data['final_datetime'] = data_hora_agendamento
        return cleaned_data

    def save(self, commit=True):
        # Pegamos a instância do agendamento mas não salvamos ainda
        instance = super().save(commit=False)
        
        # Preenchemos o campo 'date' do banco com a data que calculamos no clean()
        instance.date = self.cleaned_data['final_datetime']
        
        if commit:
            instance.save()
        return instance