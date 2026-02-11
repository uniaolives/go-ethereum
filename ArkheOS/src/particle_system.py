import numpy as np
import time

class Field:
    def __init__(self):
        self.grid = np.zeros((100, 100, 100), dtype=np.float32)

class Agent:
    def __init__(self, id):
        self.id = id
        self.health = 1.0
        self.pos = np.random.rand(3) * 100
        self.bonds = []

    def update(self, dt, field):
        # Basic movement logic
        self.pos += (np.random.rand(3) - 0.5) * dt * 10
        self.pos = np.clip(self.pos, 0, 99)
        # Interaction with field
        ix, iy, iz = self.pos.astype(int)
        if 0 <= ix < 100 and 0 <= iy < 100 and 0 <= iz < 100:
            field.grid[ix, iy, iz] += 0.01 * dt

class BioGenesisEngine:
    """Motor de simulação Bio-Gênese v3.0."""

    def __init__(self, num_agents=150):
        self.simulation_time = 0
        self.field = Field()
        self.agents = [Agent(i) for i in range(num_agents)]

    def update(self, dt=0.1):
        self.simulation_time += dt
        for agent in self.agents:
            agent.update(dt, self.field)

    def get_stats(self):
        return {
            'time': self.simulation_time,
            'agents': len(self.agents),
            'avg_health': float(np.mean([a.health for a in self.agents])) if self.agents else 0.0,
            'bonds': sum([len(a.bonds) for a in self.agents]) // 2,
            'births': 0,
            'deaths': 0
        }

    def get_agent_info(self, agent_id):
        if 0 <= agent_id < len(self.agents):
            a = self.agents[agent_id]
            return {
                'id': a.id,
                'health': float(a.health),
                'position': a.pos.tolist(),
                'bonds': len(a.bonds)
            }
        return None

    def inject_signal(self, x, y, z, strength):
        ix, iy, iz = int(x), int(y), int(z)
        if 0 <= ix < 100 and 0 <= iy < 100 and 0 <= iz < 100:
            self.field.grid[ix, iy, iz] += strength
