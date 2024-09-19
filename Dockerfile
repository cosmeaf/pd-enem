# Use uma imagem base oficial do Python
FROM python:3.12-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de requisitos (requirements.txt) para a imagem
COPY requirements.txt /app/

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o projeto para o container
COPY . /app/

# Defina a variável DJANGO_SETTINGS_MODULE para o módulo core.settings
ENV DJANGO_SETTINGS_MODULE=core.settings

# Executa o collectstatic para coletar os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Crie as pastas /app/static e /app/media se não existirem
RUN mkdir -p /app/static /app/media

# Defina permissões corretas para as pastas static e media
RUN chown -R www-data:www-data /app/static /app/media
RUN chmod -R 755 /app/static /app/media

# Exponha a porta que a aplicação irá rodar
EXPOSE 7000

# Comando para rodar o Gunicorn e iniciar a aplicação na porta 7000
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:7000", "core.wsgi:application"]
