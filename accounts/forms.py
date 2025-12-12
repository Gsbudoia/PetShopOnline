from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ClienteSignupForm(UserCreationForm):
    full_name = forms.CharField(label="Nome Completo", max_length=100)
    phone = forms.CharField(label="Telefone", max_length=20)
    email = forms.EmailField(label="E-mail", required=True)

    class Meta:
        model = CustomUser
        # Aqui é definido quais campos aparecem no HTML
        fields = ('email', 'full_name', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Percorre todos os campos e adiciona o estilo do Bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        # 1. Salva os dados no objeto User (na memória)
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Opcional: Usar o email como username para evitar erro de duplicidade
        user.username = self.cleaned_data['email'] 
        
        if commit:
            user.save()
        return user