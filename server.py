# server.py
from flask import Flask, jsonify, send_from_directory, request
from city_generator import CityMap
from hybrid_solver import HybridMazeSolver
import numpy as np

app = Flask(__name__, static_url_path='', static_folder='.')

# Global maze to persist state between clicks
current_maze = None


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# server.py (Partial Update - Replace the generate_simulation function)

@app.route('/generate', methods=['POST'])
def generate_simulation():
    global current_maze

    data = request.json
    new_map = data.get('new_map', True)
    start_pos = data.get('start', [1, 1])
    end_pos = data.get('end', [39, 39])

    # LOGIC: Define how much "thinking" the AI needs to do
    ai_episodes = 10000  # Default for new maps

    if new_map or current_maze is None:
        print("⚡ Generating NEW City Layout...")
        current_maze = CityMap(width=41, height=41)
        current_maze.generate_manhattan_grid()
    else:
        # If just recalculating, use fewer episodes for speed
        print("⚡ Recalculating on existing map (Fast Mode)...")
        ai_episodes = 2500

        # Update Start/End
    if current_maze.grid[start_pos[0], start_pos[1]] == 1:
        print("Warning: Start point is inside a building.")
    else:
        current_maze.start = tuple(start_pos)

    if current_maze.grid[end_pos[0], end_pos[1]] == 1:
        print("Warning: End point is inside a building.")
    else:
        current_maze.end = tuple(end_pos)

    # Solve with variable effort
    solver = HybridMazeSolver(current_maze)
    path = solver.solve(training_episodes=ai_episodes)

    status = "success" if path else "error"

    response = {
        "status": status,
        "dimensions": {"width": current_maze.width, "height": current_maze.height},
        "grid": current_maze.grid.astype(int).tolist(),
        "traffic": current_maze.traffic_jams.tolist(),
        "conductivity": solver.conductivity.tolist(),
        "path": path,
        "start": current_maze.start,
        "end": current_maze.end
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5000)