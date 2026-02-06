import json
import numpy as np


def export_simulation(maze, conductivity, path, filename="traffic_data.json"):
    """
    Exports the generated city, slime mold data, and calculated path to JSON.
    """
    # Convert NumPy arrays to standard lists for JSON serialization
    data = {
        "dimensions": {
            "width": maze.width,
            "height": maze.height
        },
        # 1 = Building, 0 = Road
        "grid": maze.grid.astype(int).tolist(),

        # Traffic intensity map
        "traffic": maze.traffic_jams.tolist(),

        # Slime mold conductivity (0.0 to 1.0)
        "conductivity": conductivity.tolist(),

        # The final Q-Learning path [(x,y), (x,y)...]
        "path": path
    }

    with open(filename, "w") as f:
        json.dump(data, f)
    print(f"✅ Simulation data saved to {filename}")