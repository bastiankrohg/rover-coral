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