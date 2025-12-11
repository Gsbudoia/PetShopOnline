# Usa uma imagem leve do Python
FROM python:3.9-slim

# Evita que o Python gere arquivos .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala as dependências do sistema necessárias para o Postgres
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements e instala as bibliotecas
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o resto do projeto
COPY . /app/

# Comando para rodar o servidor (no dia da apresentação, usaremos Gunicorn, mas pro teste pode ser runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]