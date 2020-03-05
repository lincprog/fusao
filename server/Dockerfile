FROM python:3.6.2

ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /server
# "Copia" arquivo requirements.txt para o diretorio
COPY requirements.txt /server/

# Executa o pip
RUN pip install -r requirements.txt