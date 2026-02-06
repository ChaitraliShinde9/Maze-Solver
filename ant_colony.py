# ant_colony.py
import numpy as np


class AntColonySolver:
    def __init__(self, maze, num_ants=20, num_iterations=50,
                 alpha=1.0, beta=2.0, evaporation=0.5,
                 initial_pheromone=None):
        self.maze = maze
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha  # Pheromone importance
        self.beta = beta  # Heuristic importance
        self.evaporation = evaporation

        # Initialize pheromone matrix
        if initial_pheromone is not None:
            # Use slime mold conductivity as initial pheromones
            self.pheromones = initial_pheromone.copy()
        else:
            self.pheromones = np.ones((maze.height, maze.width))

        self.pheromones[maze.grid == 1] = 0

        self.best_path = None
        self.best_length = float('inf')

    def heuristic(self, current, neighbor):
        """Distance-based heuristic (closer to goal = better)"""
        goal = self.maze.end
        dist = np.sqrt((neighbor[0] - goal[0]) ** 2 +
                       (neighbor[1] - goal[1]) ** 2)
        return 1.0 / (dist + 1)  # Avoid division by zero

    def select_next(self, current, visited):
        """Probabilistic path selection"""
        neighbors = self.maze.get_neighbors(current)
        neighbors = [n for n in neighbors if n not in visited]

        if not neighbors:
            return None

        # Calculate probabilities
        probabilities = []
        for neighbor in neighbors:
            tau = self.pheromones[neighbor[0], neighbor[1]]
            eta = self.heuristic(current, neighbor)
            prob = (tau ** self.alpha) * (eta ** self.beta)
            probabilities.append(prob)

        # Normalize
        total = sum(probabilities)
        if total == 0:
            return np.random.choice(neighbors)

        probabilities = np.array(probabilities) / total

        # Roulette wheel selection
        idx = np.random.choice(len(neighbors), p=probabilities)
        return neighbors[idx]

    def construct_solution(self):
        """Single ant constructs a path"""
        path = [self.maze.start]
        visited = set(path)
        current = self.maze.start

        max_steps = self.maze.height * self.maze.width
        steps = 0

        while current != self.maze.end and steps < max_steps:
            next_pos = self.select_next(current, visited)
            if next_pos is None:
                return None  # Dead end

            path.append(next_pos)
            visited.add(next_pos)
            current = next_pos
            steps += 1

        if current == self.maze.end:
            return path
        return None

    def update_pheromones(self, all_paths):
        """Update pheromone levels"""
        # Evaporation
        self.pheromones *= (1 - self.evaporation)

        # Deposit pheromones
        for path in all_paths:
            if path is not None:
                deposit = 1.0 / len(path)  # Shorter paths get more pheromone
                for pos in path:
                    self.pheromones[pos[0], pos[1]] += deposit

    def solve(self):
        """Main ACO loop"""
        for iteration in range(self.num_iterations):
            # All ants construct solutions
            all_paths = []
            for _ in range(self.num_ants):
                path = self.construct_solution()
                if path is not None:
                    all_paths.append(path)

                    # Track best path
                    if len(path) < self.best_length:
                        self.best_path = path
                        self.best_length = len(path)

            # Update pheromones
            self.update_pheromones(all_paths)

            print(f"Iteration {iteration + 1}: Best length = {self.best_length}")

        return self.best_path
