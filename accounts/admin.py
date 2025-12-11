from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Registra o nosso usuário usando a interface padrão de usuários do Django
admin.site.register(CustomUser, UserAdmin)