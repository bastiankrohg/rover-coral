# visualization/plotter.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Visualizer:
    def __init__(self, grid_size, obstacles, resources):
        self.grid_size = grid_size
        self.obstacles = obstacles
        self.resources = resources
        self.fig, self.ax = plt.subplots()
        self._setup_plot()

    def _setup_plot(self):
        self.ax.set_xlim(0, self.grid_size[0])
        self.ax.set_ylim(0, self.grid_size[1])
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self._plot_obstacles()
        self._plot_resources()

    def _plot_obstacles(self):
        for obs in self.obstacles:
            rect = patches.Rectangle((obs[0], obs[1]), 1, 1, facecolor='gray')
            self.ax.add_patch(rect)

    def _plot_resources(self):
        for res in self.resources:
            circle = patches.Circle((res[0] + 0.5, res[1] + 0.5), 0.3, facecolor='green')
            self.ax.add_patch(circle)

    def plot_path(self, path, color='red'):
        if path:
            x, y = zip(*path)
            self.ax.plot(x, y, linestyle='--', color=color, marker='o')

    def plot_rover(self, position, heading, size):
        x, y = position
        width = size
        height = size * 0.5

        # Create a rectangle to represent the rover
        rover_body = patches.Rectangle(
            (x - width / 2, y - height / 2),
            width,
            height,
            angle=np.degrees(heading),
            edgecolor='blue',
            facecolor='none'
        )
        self.ax.add_patch(rover_body)

        # Plot heading direction
        head_x = x + (width / 2) * np.cos(heading)
        head_y = y + (width / 2) * np.sin(heading)
        self.ax.plot([x, head_x], [y, head_y], color='blue')

    def update(self, rover, optimal_path):
        self.ax.clear()
        self._setup_plot()
        self.plot_path(optimal_path, color='red')
        self.plot_path(rover.traveled_path, color='blue')
        self.plot_rover(rover.position, rover.heading, rover.size)
        plt.draw()
        plt.pause(0.01)

    def display_final(self):
        """
        Display the final state of the plot.
        """
        print("Displaying final visualization...")
        plt.show()
