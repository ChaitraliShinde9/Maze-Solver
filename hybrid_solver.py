# hybrid_solver.py
from slime_mold import SlimeMoldSolver
from q_learning import QLearningSolver


class HybridMazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.slime_solver = SlimeMoldSolver(maze)
        self.conductivity = None
        self.final_path = None

    # ADD 'training_episodes' parameter here
    def solve(self, training_episodes=15000):
        """Execute Smart City Logic"""
        print(f"Phase 1: Slime Mold Traffic Sensor Network...")
        self.conductivity = self.slime_solver.solve()

        print(f"\nPhase 2: Autonomous Car AI (Training {training_episodes} episodes)...")

        # Use the variable instead of hardcoded 15000
        self.rl_solver = QLearningSolver(
            self.maze,
            conductivity_map=self.conductivity,
            episodes=training_episodes
        )

        self.final_path = self.rl_solver.solve()
        return self.final_path