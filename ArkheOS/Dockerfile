# ArkheOS/Dockerfile
FROM python:3.11-slim-bookworm

# Metadados do Sistema
LABEL org.opencontainers.image.title="Arkhe(n) Core OS"
LABEL org.opencontainers.image.description="Sistema Operacional Biológico com Hebbian Scheduling"
LABEL org.opencontainers.image.version="1.0.0-alpha"

# Configuração do sistema base
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    procps \
    htop \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configura diretório de trabalho
WORKDIR /arkhe

# Copia dependências primeiro (para cache eficiente)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia código fonte
COPY src/ /arkhe/src/

# Configura ambiente
ENV PYTHONPATH=/arkhe
ENV PYTHONUNBUFFERED=1
ENV PYGLET_HEADLESS=1
ENV ARKHE_MODE=container
ENV OMP_NUM_THREADS=2

# Cria diretórios para dados persistentes
RUN mkdir -p /arkhe/data /arkhe/logs /arkhe/shared

# Expõe porta MCP
EXPOSE 8000

# Ponto de entrada
ENTRYPOINT ["python", "-m", "src.main"]
