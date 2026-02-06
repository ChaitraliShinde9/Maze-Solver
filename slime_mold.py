# slime_mold.py
import numpy as np

class SlimeMoldSolver:
    def __init__(self, maze, num_agents=50, max_iters=100):
        self.maze = maze
        self.num_agents = num_agents
        self.max_iters = max_iters
        self.z = 0.05  # Reduced random exploration to stay focused

        # Initialize conductivity
        self.conductivity = np.ones((maze.height, maze.width))
        # Zero conductivity on buildings
        self.conductivity[maze.grid == 1] = 0

        # PENALIZE TRAFFIC in the base conductivity
        # If traffic is 5.0, conductivity becomes very low (e.g., 0.1)
        # Formula: 1.0 / (1.0 + traffic_intensity)
        traffic_factor = 1.0 / (1.0 + maze.traffic_jams)
        self.conductivity *= traffic_factor

    def objective_function(self, position):
        x, y = position
        goal_x, goal_y = self.maze.end

        # Distance Cost
        dist = np.sqrt((x - goal_x) ** 2 + (y - goal_y) ** 2)

        # Traffic Cost (If on a traffic spot, add massive penalty)
        # We assume position is roughly integer for lookup
        ix, iy = int(x), int(y)
        traffic_cost = 0
        if 0 <= ix < self.maze.height and 0 <= iy < self.maze.width:
            traffic_cost = self.maze.traffic_jams[ix, iy] * 10  # Massive penalty

        return dist + traffic_cost

    def initialize_positions(self):
        positions = []
        for _ in range(self.num_agents):
            while True:
                x = np.random.randint(0, self.maze.height)
                y = np.random.randint(0, self.maze.width)
                if self.maze.is_valid(x, y):
                    positions.append((x, y))
                    break
        return np.array(positions)

    def solve(self):
        positions = self.initialize_positions()
        w = 0.9  # Weight parameter

        for iteration in range(self.max_iters):
            fitness = np.array([self.objective_function(pos) for pos in positions])
            sorted_idx = np.argsort(fitness)
            positions = positions[sorted_idx]
            best_pos = positions[0]

            w = w * np.exp(-iteration / self.max_iters)

            for j in range(self.num_agents):
                if np.random.random() < w:
                    direction = best_pos - positions[j]
                    new_pos = positions[j] + np.random.rand() * direction
                else:
                    rand_idx = np.random.randint(0, self.num_agents)
                    direction = positions[rand_idx] - positions[j]
                    new_pos = positions[j] + self.z * np.random.rand() * direction

                new_pos = np.clip(new_pos, [0, 0], [self.maze.height - 1, self.maze.width - 1])
                new_pos = new_pos.astype(int)

                if self.maze.is_valid(new_pos[0], new_pos[1]):
                    self.conductivity[new_pos[0], new_pos[1]] += 0.1
                    positions[j] = new_pos

        self.conductivity = self.conductivity / np.max(self.conductivity)
        return self.conductivity