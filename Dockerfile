# Etapa 1: Construção da imagem base
FROM python:3.9-slim as builder

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o diretório de trabalho
COPY ./app /app

# Etapa 2: Construção da imagem final
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Defina argumentos de build
ARG MONGO_USER=${MONGO_USER}
ARG MONGO_PASS=${MONGO_PASS}

# Defina variáveis de ambiente
ENV MONGO_USER=${MONGO_USER}
ENV MONGO_PASS=${MONGO_PASS}

# Defina o diretório de trabalho no container
WORKDIR /code

# Copie as dependências instaladas da etapa anterior
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /code

# Defina permissões para o diretório de trabalho
RUN chmod -R 755 /code

# Exponha a porta
EXPOSE $PORT

# Defina o comando para iniciar a aplicação
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]