from django.contrib import admin
from .models import Customer, Pet

# Configuração para editar Pets dentro da tela do Cliente
class PetInline(admin.TabularInline):
    model = Pet
    extra = 1  # Quantos campos em branco aparecem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'email')
    inlines = [PetInline]  # Aqui ativamos o Inline

admin.site.register(Pet)