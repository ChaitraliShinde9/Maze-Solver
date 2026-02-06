# In main.py
from city_generator import CityMap
from hybrid_solver import HybridMazeSolver
from exporter import export_simulation  # Import the new function

def main():
    print("Generating City...")
    maze = CityMap(width=41, height=41)
    maze.generate_manhattan_grid()

    print("Solving...")
    solver = HybridMazeSolver(maze)
    path = solver.solve()

    if path:
        print(f"Solution Found! Length: {len(path)}")
        # REPLACE visualizer calls with this:
        export_simulation(maze, solver.conductivity, path)
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()