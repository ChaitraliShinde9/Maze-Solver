# q_learning.py
import numpy as np
import random
import time


class QLearningSolver:
    def __init__(self, maze, conductivity_map=None, episodes=5000, alpha=0.1, gamma=0.95):
        self.maze = maze
        self.conductivity = conductivity_map
        self.episodes = episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_decay = 0.9992
        self.min_epsilon = 0.05
        self.q_table = np.zeros((maze.height, maze.width, 4))
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_valid_actions(self, pos):
        valid = []
        x, y = pos
        for idx, (dx, dy) in enumerate(self.actions):
            nx, ny = x + dx, y + dy
            if self.maze.is_valid(nx, ny):
                valid.append(idx)
        return valid

    def get_reward(self, current_pos, next_pos):
        if next_pos == self.maze.end: return 1000
        reward = -1
        # Traffic
        if hasattr(self.maze, 'traffic_jams'):
            sev = self.maze.traffic_jams[next_pos[0], next_pos[1]]
            if sev > 0: reward -= (sev * 2)
        # Slime
        if self.conductivity is not None:
            reward += self.conductivity[next_pos[0], next_pos[1]] * 2
        # Heuristic (Compass)
        goal = self.maze.end
        curr_dist = abs(current_pos[0] - goal[0]) + abs(current_pos[1] - goal[1])
        next_dist = abs(next_pos[0] - goal[0]) + abs(next_pos[1] - goal[1])
        if next_dist < curr_dist:
            reward += 0.5
        else:
            reward -= 0.5
        return reward

    def solve(self):
        print(f"TRAINING AI ({self.episodes} episodes)...")
        for episode in range(1, self.episodes + 1):
            current = self.maze.start
            steps = 0
            while current != self.maze.end and steps < 1500:
                x, y = current
                if random.random() < self.epsilon:
                    valid = self.get_valid_actions(current)
                    if not valid: break
                    idx = random.choice(valid)
                else:
                    idx = np.argmax(self.q_table[x, y] + np.random.randn(4) * 1e-5)

                dx, dy = self.actions[idx]
                next_pos = (x + dx, y + dy)

                if not self.maze.is_valid(next_pos[0], next_pos[1]):
                    # Hit building
                    self.q_table[x, y, idx] = (1 - self.alpha) * self.q_table[x, y, idx] + self.alpha * -50
                    continue

                reward = self.get_reward(current, next_pos)
                nx, ny = next_pos
                max_q = np.max(self.q_table[nx, ny])
                curr_q = self.q_table[x, y, idx]
                self.q_table[x, y, idx] = curr_q + self.alpha * (reward + self.gamma * max_q - curr_q)

                current = next_pos
                steps += 1

            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay

        return self.reconstruct_path()

    def reconstruct_path(self):
        path = [self.maze.start]
        current = self.maze.start
        visited = set([current])
        while current != self.maze.end:
            x, y = current
            idx = np.argmax(self.q_table[x, y])
            dx, dy = self.actions[idx]
            next_pos = (x + dx, y + dy)
            if next_pos in visited or not self.maze.is_valid(next_pos[0], next_pos[1]): break
            path.append(next_pos)
            visited.add(next_pos)
            current = next_pos
            if len(path) > 1500: break
        return path