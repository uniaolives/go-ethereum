#!/usr/bin/env python3
"""
ARKHE(N) BOOTLOADER v1.3
Inicializa o sistema Arkhe(n) com suporte a MCP e simulação concorrente.
"""

import asyncio
import logging
import sys
import threading
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(name)s]: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ArkheBoot')

# Importação segura de módulos do sistema
try:
    from src.particle_system import BioGenesisEngine
    from src.shared_memory import SharedFieldManager
    BIOGENESIS_LOADED = True
except ImportError:
    try:
        from .particle_system import BioGenesisEngine
        from .shared_memory import SharedFieldManager
        BIOGENESIS_LOADED = True
    except ImportError as e:
        logger.error(f"❌ Falha ao carregar módulos internos: {e}")
        BIOGENESIS_LOADED = False
        BioGenesisEngine = None
        SharedFieldManager = None

# Importação segura do FastMCP
try:
    from fastmcp import FastMCP
except ImportError:
    logger.warning("⚠️ FastMCP não encontrado. O servidor MCP poderá falhar.")
    FastMCP = None

# Instância global do sistema
engine = BioGenesisEngine(num_agents=150) if BioGenesisEngine else None
shared_field = SharedFieldManager() if SharedFieldManager else None

# Definição do Servidor MCP
if FastMCP:
    mcp = FastMCP("Arkhe(n) Core OS")

    @mcp.tool()
    async def get_system_status():
        """Retorna telemetria vital do sistema operacional Arkhe."""
        if engine is None:
            return {"status": "ERROR", "message": "Motor de simulação não carregado"}
        stats = engine.get_stats()
        return {
            "status": "OPERATIONAL",
            "agents_alive": stats['agents'],
            "simulation_time": stats['time'],
            "average_health": stats['avg_health'],
            "field_active": shared_field and shared_field.field is not None
        }

    @mcp.tool()
    async def inject_field_signal(x: float, y: float, z: float, strength: float):
        """Injeta um sinal no campo morfogenético na posição (x,y,z)."""
        if engine:
            engine.inject_signal(x, y, z, strength)
            return f"Sinal de força {strength} injetado em ({x}, {y}, {z})."
        return "Erro: Simulação não disponível."
else:
    mcp = None

def run_simulation_sync():
    """Ponto de entrada síncrono para a thread de simulação."""
    if not engine or not shared_field:
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def simulation_loop():
        logger.info("🌌 Inicializando Campo Morfogenético...")
        await shared_field.initialize()

        logger.info("🧠 Iniciando loop de simulação (10Hz)...")
        while True:
            try:
                # Atualiza simulação
                engine.update(dt=0.1)

                # Sincroniza com campo compartilhado
                if shared_field.field is not None:
                    shared_field.update_field(engine.field.grid)

            except Exception as e:
                logger.error(f"Erro no loop de simulação: {e}")

            await asyncio.sleep(0.1)

    loop.run_until_complete(simulation_loop())

if __name__ == "__main__":
    logger.info("🚀 Arkhe(n) Core OS Booting...")

    # Inicia a simulação em uma thread separada
    if engine:
        sim_thread = threading.Thread(target=run_simulation_sync, daemon=True)
        sim_thread.start()
    else:
        logger.warning("⚠️  Simulação desativada (engine não carregado)")

    # Inicia o servidor MCP (Bloqueante)
    if mcp:
        try:
            logger.info("🔌 Servidor MCP ativo (Transport: SSE)")
            # run() é bloqueante em muitas implementações de FastMCP
            mcp.run(transport="sse")
        except Exception as e:
            logger.error(f"Erro fatal no servidor MCP: {e}")
            sys.exit(1)
    else:
        logger.critical("❌ Servidor MCP não pôde ser iniciado.")
        # Mantém vivo para log se a simulação estiver rodando
        if engine:
            while True: time.sleep(1)
        sys.exit(1)
