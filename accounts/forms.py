from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ClienteSignupForm(UserCreationForm):
    # Adicionamos os campos que faltam para o modelo Customer
    full_name = forms.CharField(label="Nome Completo", max_length=100)
    phone = forms.CharField(label="Telefone", max_length=20)
    email = forms.EmailField(label="E-mail", required=True)

    class Meta:
        model = CustomUser
        # Aqui definimos quais campos aparecem no HTML
        fields = ('email', 'full_name', 'phone')

    def save(self, commit=True):
        # 1. Salva os dados no objeto User (na memória)
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Opcional: Usar o email como username para evitar erro de duplicidade
        user.username = self.cleaned_data['email'] 
        
        if commit:
            user.save()
        return user