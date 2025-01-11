# rover.py

import time
import math
import numpy as np
from algorithms.a_star import a_star

class Rover:
    def __init__(self, start_position, grid_size, obstacles, resources, size=1.0, nominal_speed=1.0, turn_radius=1.0, turning_speed=np.pi/4):
        self.position = np.array(start_position, dtype='float64')
        self.grid_size = grid_size
        self.obstacles = set(obstacles)
        self.resources = set(resources)
        self.size = size
        self.nominal_speed = nominal_speed
        self.turn_radius = turn_radius
        self.turning_speed = turning_speed
        self.heading = 0.0  # In radians; 0 means facing right
        self.traveled_path = [tuple(self.position)]
        self.optimal_path = []
        self.resource_registry = set()
        self.verified_resources = []
        self.total_distance_traveled = 0.0
        self.fov_angle = np.pi / 4  # 45 degrees

    def report_state(self):
            """
            Report the initial state of the rover.
            """
            print("Rover System State:")
            print(f"Position: {self.position}")
            print(f"Heading: {np.degrees(self.heading)} degrees")
            print(f"Grid size: {self.grid_size}")
            print(f"Obstacles: {self.obstacles}")
            print(f"Resources: {self.resources}")
            print(f"Traveled Path: {self.traveled_path}")

    def move_to(self, waypoint):
        print(f"Moving to {waypoint}...")
        target_position = np.array(waypoint, dtype='float64')
        direction = target_position - self.position
        distance = np.linalg.norm(direction)

        if distance > 0:
            step = direction / distance * self.nominal_speed * 0.1
            steps = int(distance // np.linalg.norm(step))

            for _ in range(steps):
                next_position = self.position + step
                if self.is_within_bounds(next_position) and not self.is_collision(next_position):
                    self.position = next_position
                    self.traveled_path.append(tuple(np.floor(self.position).astype(int)))
                    self.total_distance_traveled += np.linalg.norm(step)
                else:
                    print("Movement blocked by obstacle or boundary.")
                    break

            self.position = target_position
            self.traveled_path.append(tuple(np.floor(self.position).astype(int)))
            self.total_distance_traveled += distance

        print(f"Arrived at {waypoint}. Total distance traveled: {self.total_distance_traveled:.2f}.")

    def perform_360_scan(self):
        """
        Perform a 360-degree scan in 45-degree increments.
        """
        print("Starting 360-degree scan...")
        detected_resources = []
        for step in range(8):
            self.heading = (self.heading + np.pi / 4) % (2 * np.pi)  # Increment by 45 degrees
            print(f"Scanning at heading: {np.degrees(self.heading):.1f} degrees")

            # Simulate ultrasound measurement
            print(f"Ultrasound measurement: Simulated distance to object.")

            # Simulate picture capture
            print(f"Picture taken at heading {np.degrees(self.heading):.1f} degrees.")

            # Dummy resource detection logic
            for resource in self.resources:
                if self._distance_to(resource) <= 50 and self._is_facing(resource):
                    print(f"Resource detected: {resource}")
                    detected_resources.append(resource)
                    self.resource_registry.add(resource)

        return detected_resources
    
    def explore(self):
        """
        Explore surroundings using a search pattern and obstacle avoidance.
        """
        print("No resources detected. Generating search pattern...")
        pattern = self.generate_expanding_square_pattern()

        for waypoint in pattern:
            if waypoint in self.obstacles:
                print(f"Waypoint {waypoint} blocked by obstacle. Modifying path...")
                continue  # Skip obstacle or recompute path
            self.move_to(waypoint)
            detected_resources = self.perform_360_scan()
            if detected_resources:
                print(f"Resources found during exploration: {detected_resources}")
                break

    def search_area(self):
        print("Searching area...")
        detected_resources = self.perform_360_scan()

        if detected_resources:
            print(f"Resources found during search: {detected_resources}")

        # Generate an expanding square search pattern
        print("No new resources nearby. Continuing expanding square search...")
        pattern = self.generate_expanding_square_pattern()
        # use from pattern/expanding_square.py?

        for waypoint in pattern:
            if waypoint not in self.traveled_path and waypoint not in self.obstacles:
                print(f"Moving to {waypoint} as part of search.")
                self.move_to(waypoint)
                self.perform_360_scan()

    def switch_mode(self, new_mode):
        self.mode = new_mode
        print(f"Switched to {new_mode} mode.")

    def navigate_to(self, target):
        print(f"Navigating to {target}...")
        self.path = a_star(self.position, target, self.obstacles, self.grid_size)
        if not self.path:
            print("No path found to the target.")
            return False
        for waypoint in self.path:
            self.move_to(waypoint)
            if self.detect_obstacle_ahead():
                print("Obstacle detected! Recomputing path...")
                self.avoid_obstacle()
                return False
        print("Reached the target.")
        return True
    
    def navigate_to_waypoints(self, waypoints, threshold=1.0):
        """
        Navigate to a series of waypoints with a completion threshold.

        Parameters:
        - waypoints: List of (x, y) waypoints to navigate to.
        - threshold: Distance within which the waypoint is considered reached.
        """
        for waypoint in waypoints:
            print(f"Navigating to waypoint: {waypoint}")

            # Check if already within the threshold distance
            if self._distance_to(waypoint) <= threshold:
                print(f"Waypoint {waypoint} already reached (within {threshold} units).")
                continue

            # Calculate path using A*
            path = a_star(tuple(self.position), waypoint, self.obstacles, self.grid_size)

            if not path:
                print(f"Unable to find a path to waypoint {waypoint}. Skipping.")
                continue

            # Move along the calculated path
            for step in path:
                self.move_to(step)
                if self._distance_to(waypoint) <= threshold:
                    print(f"Waypoint {waypoint} reached (within {threshold} units).")
                    break

            print(f"Arrived at waypoint: {waypoint}")
    
    def navigate_to_resource(self, resource):
        """
        Navigate toward a detected resource and verify it upon arrival.
        """
        print(f"Navigating to resource at {resource}...")
        path = a_star(tuple(self.position), resource, self.obstacles, self.grid_size)
        if not path:
            print(f"No valid path to resource at {resource}.")
            return
        self.navigate_to(resource)

        # Verify the resource
        if self.verify_resource(resource):
            print(f"Resource at {resource} verified.")
            self.resources.remove(resource)

    def verify_resource(self, resource):
        """
        Verify if a resource is within 5 units and in FOV.
        """
        if self._distance_to(resource) <= 5 and self._is_facing(resource):
            if resource not in self.verified_resources:
                self.verified_resources.append(resource)
                print(f"Resource verified: {resource}")
                return True
        return False

    def detect_obstacle_ahead(self):
        next_position = self.path[0] if self.path else self.position
        return next_position in self.obstacles

    def avoid_obstacle(self):
        print("Avoiding obstacle...")
        self.switch_mode('search')

    def _distance_to(self, target):
        """
        Calculate Euclidean distance to a target point.

        Parameters:
        - target: (x, y) coordinates of the target point.

        Returns:
        - Distance to the target point.
        """
        target_position = np.array(target, dtype='float64')
        return np.linalg.norm(self.position - target_position)

    def _is_facing(self, target):
        """
        Check if the rover is facing the target within its field of view (FOV).
        """
        direction_vector = np.array(target) - self.position
        angle_to_target = math.atan2(direction_vector[1], direction_vector[0])
        angle_diff = abs((self.heading - angle_to_target + np.pi) % (2 * np.pi) - np.pi)
        return angle_diff <= self.fov_angle / 2

    def detect_resources(self):
        """
        Detect resources within a certain distance and in the rover's field of view (FOV).
        Returns a list of detected resources.
        """
        print("Detecting resources...")
        detected = []
        for resource in self.resources:
            # Check if the resource is within the detection range (50 units) and in the rover's FOV
            if self._distance_to(resource) <= 50 and self._is_facing(resource):
                detected.append(resource)
                self.resource_registry.add(resource)  # Add to registry if detected
        print(f"Detected resources: {detected}")
        return detected

    def generate_expanding_square_pattern(self):
        print("Generating expanding square search pattern...")
        pattern = []
        x, y = self.position
        step = 1
        while len(pattern) < 20:
            for _ in range(step):
                x += 1
                if self.is_within_bounds((x, y)):
                    pattern.append((x, y))
            for _ in range(step):
                y += 1
                if self.is_within_bounds((x, y)):
                    pattern.append((x, y))
            step += 1
            for _ in range(step):
                x -= 1
                if self.is_within_bounds((x, y)):
                    pattern.append((x, y))
            for _ in range(step):
                y -= 1
                if self.is_within_bounds((x, y)):
                    pattern.append((x, y))
            step += 1
        print(f"Expanding square pattern: {pattern}")
        return pattern

#    def is_within_bounds(self, position):
#        x, y = position
#        return 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]

    def is_within_bounds(self, position):
        """
        Check if the given position is within the grid boundaries.
        
        Parameters:
        - position: The (x, y) position to check, can be a tuple or numpy array.

        Returns:
        - True if the position is within bounds, False otherwise.
        """
        x, y = map(int, tuple(position))  # Ensure position is a tuple of integers
        return self.grid_size[0][0] <= x < self.grid_size[0][1] and self.grid_size[1][0] <= y < self.grid_size[1][1]

    def is_collision(self, position):
        """
        Check if the given position collides with an obstacle.
        """
        return tuple(np.floor(position).astype(int)) in self.obstacles
    
    def main_loop(self):
        while True:
            if self.mode == 'search':
                target = self.search_area()
                if target:
                    self.switch_mode('navigate')
            elif self.mode == 'navigate':
                if self.path:
                    target = self.path[-1]
                    if self.navigate_to(target):
                        self.resources.discard(target)
                        self.switch_mode('search')
                else:
                    self.switch_mode('search')
            time.sleep(0.1)