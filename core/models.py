from django.db import models
from django.conf import settings # Importa o usuário

class Customer(models.Model):
    
    #Liga o cadastro ao Login do usuário
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Pet(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True, verbose_name="Raça")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Nascimento")
    photo = models.ImageField(upload_to='pets/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner.name})"