"""
Gerenciador de Memória Compartilhada para o Campo Morfogenético.
Implementa acesso de alta performance à RAM via /dev/shm.
"""

import numpy as np
import mmap
import os
import struct
import asyncio
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SharedFieldManager:
    """Gerencia o campo morfogenético em memória compartilhada."""

    def __init__(self, shm_path: str = "/dev/shm/morphogenetic_field"):
        self.shm_path = shm_path
        self.size = 100 * 100 * 100 * 4  # 100x100x100 floats (4 bytes)
        self.mmap = None
        self.field = None

    async def initialize(self):
        """Inicializa a memória compartilhada."""
        try:
            # Verifica existência antes de abrir
            exists = os.path.exists(self.shm_path)

            # Cria ou abre arquivo de memória compartilhada
            if exists:
                fd = os.open(self.shm_path, os.O_RDWR)
                logger.info(f"📂 Campo existente aberto: {self.shm_path}")
            else:
                os.makedirs(os.path.dirname(self.shm_path), exist_ok=True)
                fd = os.open(self.shm_path, os.O_CREAT | os.O_RDWR, 0o666)
                os.ftruncate(fd, self.size)
                logger.info(f"🆕 Campo criado: {self.shm_path}")

            # Mapeia na memória
            self.mmap = mmap.mmap(fd, self.size, mmap.MAP_SHARED,
                                  mmap.PROT_READ | mmap.PROT_WRITE)
            os.close(fd)

            # Cria view NumPy (zero-copy)
            self.field = np.frombuffer(self.mmap, dtype=np.float32).reshape((100, 100, 100))

            # Inicializa com zeros se for novo
            if not exists:
                self.field.fill(0.0)
                logger.info("🧹 Campo inicializado com zeros")

            logger.info(f"✅ Campo morfogenético pronto: {self.field.shape}")
            logger.info(f"   Tamanho: {self.size / (1024**2):.1f} MB")

            return True

        except Exception as e:
            logger.error(f"❌ Falha ao inicializar SHM: {e}")
            return False

    def update_field(self, new_field: np.ndarray):
        """Atualiza o campo com novos dados (copia eficiente)."""
        if self.field is not None and new_field.shape == self.field.shape:
            np.copyto(self.field, new_field)

    def get_gradient(self, x: int, y: int, z: int) -> Optional[np.ndarray]:
        """Calcula gradiente em uma posição específica."""
        if self.field is None:
            return None

        # Garante que estamos dentro dos limites para cálculo de gradiente
        if x < 1 or x > 98 or y < 1 or y > 98 or z < 1 or z > 98:
            return np.zeros(3, dtype=np.float32)

        # Calcula gradiente por diferenças finitas
        dx = self.field[x+1, y, z] - self.field[x-1, y, z]
        dy = self.field[x, y+1, z] - self.field[x, y-1, z]
        dz = self.field[x, y, z+1] - self.field[x, y, z-1]

        return np.array([dx, dy, dz], dtype=np.float32)

    async def cleanup(self):
        """Limpa recursos da memória compartilhada."""
        if self.mmap:
            self.mmap.close()
            logger.info("🗑️  Memória compartilhada liberada")

        # Remove arquivo se existir
        try:
            if os.path.exists(self.shm_path):
                os.unlink(self.shm_path)
                logger.info(f"🗑️  Arquivo SHM removido: {self.shm_path}")
        except Exception as e:
            logger.warning(f"⚠️  Não foi possível remover SHM: {e}")
