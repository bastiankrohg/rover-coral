# rover.py

import time
import math
import numpy as np
from algorithms import a_star

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
        self.resource_registry = set()  # Track detected resources
        self.total_distance_traveled = 0.0  # Track total distance traveled

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
        print("Performing 360-degree scan...")
        detected_resources = []

        for dx in range(-1, 2):  # Check in a 3x3 grid around the rover
            for dy in range(-1, 2):
                if (dx, dy) == (0, 0):
                    continue  # Skip the rover's current position

                scan_position = (int(self.position[0] + dx), int(self.position[1] + dy))

                if scan_position in self.resources and scan_position not in self.resource_registry:
                    detected_resources.append(scan_position)
                    self.resource_registry.add(scan_position)  # Add to registry

        print(f"Detected resources: {detected_resources}")
        return detected_resources

    def search_area(self):
        print("Searching area...")
        detected_resources = self.perform_360_scan()

        if detected_resources:
            print(f"Resources found during search: {detected_resources}")

        # Generate an expanding square search pattern
        print("No new resources nearby. Continuing expanding square search...")
        pattern = self.generate_expanding_square_pattern()

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

    def detect_obstacle_ahead(self):
        next_position = self.path[0] if self.path else self.position
        return next_position in self.obstacles

    def avoid_obstacle(self):
        print("Avoiding obstacle...")
        self.switch_mode('search')

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

    def is_within_bounds(self, position):
        x, y = position
        return 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]
    
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