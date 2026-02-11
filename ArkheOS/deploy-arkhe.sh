#!/bin/bash
# deploy-arkhe.sh

echo "🧬 DEPLOY DO ARKHE(N) CORE OS"
echo "================================"

# 1. Verifica Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale primeiro."
    exit 1
fi

# 2. Inicia o sistema usando Docker Compose
echo "🚀 Iniciando Arkhe(n) Core OS via Docker Compose..."
# Executa a partir da raiz do projeto ArkheOS
docker-compose up --build -d

# 3. Verifica status
echo "⏳ Aguardando inicialização..."
sleep 5

echo ""
echo "✅ ARKHE(N) CORE OS DEPLOYADO!"
echo "================================"
echo ""
docker-compose ps
echo ""
echo "📝 LOGS:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 PARA PARAR:"
echo "   docker-compose down"
