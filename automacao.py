import os
import sys

# Função para rodar comandos no terminal
def rodar(comando):
    print(f"--> Executando: {comando}")
    retorno = os.system(comando)
    if retorno != 0:
        print(f"Erro ao executar: {comando}")
        sys.exit(1)

print("=== INICIANDO AUTOMACAO ===")

# 1. Cria as tabelas no banco
rodar("python manage.py migrate")

# 2. Cria o superusuário (usando um script inline seguro)
script_user = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@petshop.com', 'admin123')
    print('Superusuário criado com sucesso!')
else:
    print('Superusuário já existe.')
"""
# Roda o script acima
rodar(f'python -c "{script_user}"')

print("=== TUDO PRONTO! LIGANDO SERVIDOR ===")
# 3. Liga o servidor
os.system("python manage.py runserver 0.0.0.0:8000")