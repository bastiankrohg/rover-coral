# visualization/plotter.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Visualizer:
    def __init__(self, grid_size, obstacles, resources):
        self.grid_size = grid_size
        self.obstacles = obstacles
        self.resources = resources
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self._setup_plot()
        self.rover, = self.ax.plot([], [], 'ro', markersize=8)  # Red circle for the rover
        self.path_line, = self.ax.plot([], [], linestyle='-', color='red')  # Traveled path
        self.background = None

    def _setup_plot(self):
        self.ax.set_xlim(0, self.grid_size[0])
        self.ax.set_ylim(0, self.grid_size[1])
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.grid(True)

        # Plot obstacles
        for obs in self.obstacles:
            self.ax.add_patch(plt.Rectangle(obs, 1, 1, color='black'))

        # Plot resources
        for res in self.resources:
            self.ax.add_patch(plt.Rectangle(res, 1, 1, color='green'))

    def initialize_plot(self):
        """
        Draw the initial plot and cache the background for blitting.
        """
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)

    def update(self, rover_position, traveled_path, search_pattern=None):
        """
        Update the plot with the rover's current position and path.
        """
        if self.background is None:
            raise RuntimeError("Call initialize_plot() before update().")

        # Restore the cached background
        self.fig.canvas.restore_region(self.background)

        # Update search pattern if provided
        if search_pattern:
            for point in search_pattern:
                self.ax.add_patch(plt.Circle((point[0] + 0.5, point[1] + 0.5), 0.2, color='yellow', alpha=0.5))

        # Update the rover's position
        self.rover.set_data([rover_position[0] + 0.5], [rover_position[1] + 0.5])

        # Update the traveled path
        if traveled_path:
            x, y = zip(*traveled_path)
            self.path_line.set_data(x, y)

        # Redraw only the updated artists
        self.ax.draw_artist(self.rover)
        self.ax.draw_artist(self.path_line)

        # Blit the updated area
        self.fig.canvas.blit(self.fig.bbox)
        plt.pause(0.1)

    def display_final(self):
        """
        Display the final state of the plot.
        """
        print("Displaying final visualization...")
        plt.show()