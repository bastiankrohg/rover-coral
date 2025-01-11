import numpy as np

class OccupancyEnvironment: # with occupancy mapping
    def __init__(self, grid_size, obstacles, resources):
        self.grid_size = self._normalize_grid_size(grid_size)
        self.resources = resources
        self.occupancy_map = self._create_occupancy_map(obstacles)

    def _normalize_grid_size(self, grid_size):
        """
        Normalize grid_size to ensure it's a tuple of bounds.
        If an integer is provided, convert it to ((-size, size), (-size, size)).
        """
        if isinstance(grid_size, int):
            return ((-grid_size, grid_size), (-grid_size, grid_size))
        return grid_size

    def _create_occupancy_map(self, obstacles):
        """
        Create a 2D occupancy map for the grid.

        Parameters:
        - obstacles: List of (x, y) positions representing obstacles.

        Returns:
        - 2D numpy array where 1 indicates an obstacle and 0 indicates free space.
        """
        x_min, x_max = self.grid_size[0]
        y_min, y_max = self.grid_size[1]

        map_width = x_max - x_min + 1
        map_height = y_max - y_min + 1
        occupancy_map = np.zeros((map_width, map_height), dtype=int)

        for x, y in obstacles:
            if x_min <= x <= x_max and y_min <= y <= y_max:
                occupancy_map[x - x_min, y - y_min] = 1  # Mark as occupied

        return occupancy_map

class Environment:
    def __init__(self, grid_size, obstacles, resources, start_position):
        """
        Initialize the environment for the rover simulation.

        Args:
            grid_size (tuple): Dimensions of the grid (width, height).
            obstacles (list): List of obstacle positions as (x, y) tuples.
            resources (list): List of resource positions as (x, y) tuples.
            start_position (tuple): Starting position of the rover (x, y).
        """
        self.grid_size = grid_size
        self.obstacles = set(obstacles)
        self.resources = set(resources)
        self.start_position = start_position

    def is_position_valid(self, position):
        """
        Check if a position is valid (within bounds and not an obstacle).

        Args:
            position (tuple): Position to check (x, y).

        Returns:
            bool: True if valid, False otherwise.
        """
        x, y = position
        return (
            0 <= x < self.grid_size[0] and
            0 <= y < self.grid_size[1] and
            position not in self.obstacles
        )

    def remove_resource(self, position):
        """
        Remove a resource from the environment after it has been collected.

        Args:
            position (tuple): Position of the resource to remove (x, y).
        """
        if position in self.resources:
            self.resources.remove(position)

    def add_obstacle(self, position):
        """
        Add a new obstacle to the environment.

        Args:
            position (tuple): Position of the new obstacle (x, y).
        """
        if self.is_position_valid(position):
            self.obstacles.add(position)


