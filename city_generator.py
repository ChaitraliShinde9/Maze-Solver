# city_generator.py
import numpy as np
import random


class CityMap:
    def __init__(self, width=41, height=41):
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.grid = np.ones((self.height, self.width))
        self.start = (1, 1)
        self.end = (self.height - 2, self.width - 2)
        self.traffic_jams = np.zeros((self.height, self.width))

    def generate_manhattan_grid(self):
        """Generates a Dense Urban Grid"""
        # 1. Main Arteries (Wide Roads)
        # Every 4th cell is a road
        for y in range(1, self.width - 1, 4):
            self.grid[:, y] = 0

        for x in range(1, self.height - 1, 4):
            self.grid[x, :] = 0

        # 2. Add Random "Alleys" (Break up large blocks)
        for _ in range(20):
            rx = random.randint(1, self.height - 2)
            ry = random.randint(1, self.width - 2)
            # Carve a small horizontal or vertical alley
            if random.random() < 0.5:
                length = random.randint(3, 8)
                self.grid[rx, ry:min(ry + length, self.width - 1)] = 0
            else:
                length = random.randint(3, 8)
                self.grid[rx:min(rx + length, self.height - 1), ry] = 0

        # 3. Perimeter & Access
        self.grid[1, :] = 0
        self.grid[self.height - 2, :] = 0
        self.grid[:, 1] = 0
        self.grid[:, self.width - 2] = 0
        self.grid[self.start] = 0
        self.grid[self.end] = 0

        # 4. Traffic
        self.add_traffic_lines(num_lines=15)

    def add_traffic_lines(self, num_lines):
        count = 0
        attempts = 0

        # Define Safe Zones (No traffic allowed here)
        safe_radius = 4

        while count < num_lines and attempts < 200:
            x = random.randint(1, self.height - 2)
            y = random.randint(1, self.width - 2)

            # Check distance to start and end
            d_start = abs(x - self.start[0]) + abs(y - self.start[1])
            d_end = abs(x - self.end[0]) + abs(y - self.end[1])

            if d_start < safe_radius or d_end < safe_radius:
                attempts += 1
                continue

            if self.grid[x, y] == 0:
                length = random.randint(4, 8)
                # ... (rest of logic remains same as before) ...
                if self.grid[x, y + 1] == 0:
                    dx, dy = 0, 1
                elif self.grid[x + 1, y] == 0:
                    dx, dy = 1, 0
                else:
                    attempts += 1
                    continue

                for i in range(length):
                    nx, ny = x + (dx * i), y + (dy * i)
                    if 0 <= nx < self.height and 0 <= ny < self.width:
                        # Double check safe zone for every segment
                        ds = abs(nx - self.start[0]) + abs(ny - self.start[1])
                        de = abs(nx - self.end[0]) + abs(ny - self.end[1])

                        if ds > safe_radius and de > safe_radius and self.grid[nx, ny] == 0:
                            self.traffic_jams[nx, ny] = 5.0  # High penalty
                        else:
                            break
                count += 1
            attempts += 1

    def is_valid(self, x, y):
        return (0 <= x < self.height and
                0 <= y < self.width and
                self.grid[x, y] == 0)

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for nx, ny in neighbors
                if self.is_valid(nx, ny)]