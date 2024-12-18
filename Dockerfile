# Use a imagem base do Python 3.12
FROM python:3.12.3-slim

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpq-dev \
    xvfb \
    libgl1-mesa-glx \
    libx11-dev

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Atualize pip e setuptools
RUN pip install --upgrade pip setuptools wheel

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código fonte para o diretório de trabalho
COPY . .

# Exponha a porta que o Flask usará
EXPOSE 5000

# Configure o comando de inicialização para usar o Xvfb
CMD ["xvfb-run", "-a", "python", "api.py"]