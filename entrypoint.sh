#!/bin/sh

# Para o script se der erro em qualquer comando
set -e

echo "--- Rodando Migrações ---"
python manage.py migrate

echo "--- Criando Superusuário (se não existir) ---"
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@petshop.com', 'admin123')"

echo "--- Iniciando Servidor ---"
python manage.py runserver 0.0.0.0:8000