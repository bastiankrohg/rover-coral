import time
from algorithms.a_star import a_star

class Rover:
    def __init__(self, start_position, grid_size, obstacles, resources):
        """
        Initialize the rover's state and environment.

        Args:
            start_position (tuple): Starting position of the rover (x, y).
            grid_size (tuple): Dimensions of the grid (width, height).
            obstacles (list): List of obstacle positions as (x, y) tuples.
            resources (list): List of resource positions as (x, y) tuples.
        """
        self.position = start_position
        self.grid_size = grid_size
        self.obstacles = set(obstacles)
        self.resources = set(resources)
        self.mode = 'search'
        self.path = []
        self.visited = set()
        self.safety_margin = 1  # Define safety margin around obstacles

    def switch_mode(self, new_mode):
        """Switch the rover's operational mode."""
        self.mode = new_mode
        print(f"Switched to {new_mode} mode.")

    def perform_360_scan(self):
        """Simulate a 360-degree scan to detect nearby resources."""
        print("Performing 360-degree scan...")
        detected_resources = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx, dy) != (0, 0):
                    scan_position = (self.position[0] + dx, self.position[1] + dy)
                    if scan_position in self.resources and scan_position not in self.visited:
                        detected_resources.append(scan_position)
        print(f"Detected resources: {detected_resources}")
        return detected_resources

    def navigate_to(self, target):
        """
        Navigate to a target position using A* pathfinding.

        Args:
            target (tuple): Target position (x, y).

        Returns:
            bool: True if navigation is successful, False otherwise.
        """
        print(f"Navigating to {target}...")
        self.path = a_star(self.position, target, self.obstacles, self.grid_size)
        if not self.path:
            print("No path found to the target.")
            return False
        for waypoint in self.path:
            if not self.move_to(waypoint):
                print("Failed to move to waypoint, switching to search mode.")
                return False
        print(f"Reached target at {target}.")
        self.resources.discard(target)
        return True

    def move_to(self, waypoint):
        """
        Move the rover to a specified waypoint.

        Args:
            waypoint (tuple): The target waypoint (x, y).

        Returns:
            bool: True if the move is successful, False otherwise.
        """
        if waypoint in self.obstacles:
            print(f"Encountered obstacle at {waypoint}, cannot move.")
            return False
        if not self.is_within_bounds(waypoint):
            print(f"Waypoint {waypoint} is out of bounds.")
            return False

        print(f"Moving to {waypoint}...")
        self.visited.add(self.position)  # Mark current position as visited
        self.position = waypoint
        time.sleep(0.1)  # Simulate delay
        return True

    def is_within_bounds(self, position):
        """Check if a position is within the grid bounds."""
        x, y = position
        return 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]

    def generate_expanding_square_pattern(self, max_steps=20):
        """
        Generate an expanding square search pattern.

        Args:
            max_steps (int): Maximum number of steps to include in the pattern.

        Returns:
            list: A list of waypoints in the search pattern.
        """
        print("Generating expanding square search pattern...")
        pattern = []
        x, y = self.position
        step = 1
        while len(pattern) < max_steps:
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                for _ in range(step):
                    x += dx
                    y += dy
                    if self.is_within_bounds((x, y)):
                        pattern.append((x, y))
            step += 1
        print(f"Generated pattern: {pattern[:max_steps]}")
        return pattern[:max_steps]

    def search_area(self):
        """
        Search the current area for resources.

        Returns:
            tuple: Position of the detected resource, or None if none are found.
        """
        print("Searching area...")
        detected_resources = self.perform_360_scan()
        if detected_resources:
            self.switch_mode('navigate')
            return detected_resources[0]
        else:
            pattern = self.generate_expanding_square_pattern()
            for waypoint in pattern:
                if waypoint not in self.visited and waypoint not in self.obstacles:
                    if self.move_to(waypoint):
                        detected_resources = self.perform_360_scan()
                        if detected_resources:
                            self.switch_mode('navigate')
                            return detected_resources[0]
        return None