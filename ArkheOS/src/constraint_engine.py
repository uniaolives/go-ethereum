"""
Engine de Restrições Arkhe(n).
Implementa o critério de exclusão de estado.
"""

import numpy as np

class ConstraintEngine:
    def __init__(self):
        self.threshold = 0.95

    def is_admissible(self, state_vector, field_gradient):
        """Verifica se um estado é geometricamente admissível."""
        # Lógica simplificada baseada no compêndio
        projection = np.dot(state_vector, field_gradient)
        return projection < self.threshold
