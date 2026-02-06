# visualizer.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np


def show_slime_phase(maze, conductivity, title="Phase 1: Traffic Sensor Network"):
    # Dark Mode Background
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')

    # 1. DRAW BUILDINGS (Background Texture)
    # Instead of flat black, use a very dark grey for "land"
    ax.imshow(np.zeros_like(maze.grid), cmap=mcolors.ListedColormap(['#1E1E1E']), zorder=0)

    # 2. DRAW ROADS
    # We use the grid to create a custom "Road Map"
    # Roads are Light Grey (#505050) to look like asphalt
    road_mask = np.ma.masked_where(maze.grid == 1, np.ones_like(maze.grid))
    ax.imshow(road_mask, cmap=mcolors.ListedColormap(['#383838']), zorder=1)

    # 3. Draw Conductivity (The Heatmap)
    # Use 'plasma' or 'inferno' for a high-tech glowing look
    im = ax.imshow(conductivity, cmap='inferno', alpha=0.6, zorder=2)

    # Custom Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Traffic Potential', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    # 4. Markers
    ax.plot(maze.start[1], maze.start[0], 'o', color='#00FF00', markersize=8, markeredgecolor='white', label='Start',
            zorder=3)
    ax.plot(maze.end[1], maze.end[0], 'o', color='#FF0000', markersize=8, markeredgecolor='white', label='End',
            zorder=3)

    ax.set_title(title, color='white', fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    plt.show()


def animate_maze_solution(maze, path, conductivity=None, title="Phase 2: Smart Navigation", interval=80):
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#050505')  # Deep Black Window
    ax.set_facecolor('#1a1a1a')  # Dark Map

    # 1. DRAW BASE LAYER (Land)
    ax.imshow(np.ones_like(maze.grid), cmap=mcolors.ListedColormap(['#1a1a1a']), zorder=0)

    # 2. DRAW ROADS (Asphalt)
    # We plot roads as grey blocks
    roads = np.ma.masked_where(maze.grid == 1, np.ones_like(maze.grid))
    ax.imshow(roads, cmap=mcolors.ListedColormap(['#404040']), zorder=1)

    # 3. DRAW ROAD MARKINGS (Dashed White Lines)
    # This creates the "Street" look
    for x in range(maze.height):
        for y in range(maze.width):
            if maze.grid[x, y] == 0:
                # Add markings only if connected
                if x + 1 < maze.height and maze.grid[x + 1, y] == 0:  # Vertical
                    ax.plot([y, y], [x - 0.2, x + 1.2], color='#606060', linestyle=':', linewidth=1, zorder=1.5)
                if y + 1 < maze.width and maze.grid[x, y + 1] == 0:  # Horizontal
                    ax.plot([y - 0.2, y + 1.2], [x, x], color='#606060', linestyle=':', linewidth=1, zorder=1.5)

    # 4. TRAFFIC CLUSTERS (Glowing Red)
    if hasattr(maze, 'traffic_jams'):
        traffic_mask = np.ma.masked_where(maze.traffic_jams == 0, maze.traffic_jams)
        # 'hot' colormap makes it look like a heat signature
        ax.imshow(traffic_mask, cmap='hot', alpha=0.7, zorder=2)
        # Dummy for legend
        ax.plot([], [], 'r-', linewidth=3, label='Heavy Traffic')

    # 5. CAR PATH (Neon Cyan)
    # 'solid_capstyle' makes the line ends round, not square
    line, = ax.plot([], [], color='#00FFFF', linewidth=4, alpha=1.0,
                    solid_capstyle='round', label='AI Route', zorder=4)

    # Add a "Glow" effect under the path (Second wider, transparent line)
    glow, = ax.plot([], [], color='#00FFFF', linewidth=12, alpha=0.3,
                    solid_capstyle='round', zorder=3)

    # 6. Markers (GPS Style)
    ax.plot(maze.start[1], maze.start[0], 'o', color='#00FF00', markersize=10,
            markeredgecolor='white', markeredgewidth=2, label='Start', zorder=5)
    ax.plot(maze.end[1], maze.end[0], 'o', color='#FF0000', markersize=10,
            markeredgecolor='white', markeredgewidth=2, label='End', zorder=5)

    ax.set_title(title, color='white', fontsize=18, fontweight='bold', pad=15)

    # Minimalist Legend
    legend = ax.legend(loc='upper right', framealpha=0.95, facecolor='#202020', edgecolor='#404040')
    for text in legend.get_texts():
        text.set_color("white")

    ax.axis('off')

    path_array = np.array(path)

    def init():
        line.set_data([], [])
        glow.set_data([], [])
        return line, glow

    def update(frame):
        x_data = path_array[:frame + 1, 1]
        y_data = path_array[:frame + 1, 0]
        line.set_data(x_data, y_data)
        glow.set_data(x_data, y_data)
        return line, glow

    ani = animation.FuncAnimation(
        fig, update, init_func=init,
        frames=len(path), interval=interval, blit=True, repeat=False
    )
    plt.tight_layout()
    plt.show()