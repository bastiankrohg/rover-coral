import matplotlib.pyplot as plt
import numpy as np
import time
import math
from path_generator import generate_sine_wave, generate_expanding_square
from movement_commands import calculate_commands
from commands import Command

class PathFollower:
    def __init__(self, path, look_ahead_distance=2.0, grid_size=(50, 50), initial_heading=0.0):
        self.path = path
        self.current_position = np.array(path[0], dtype="float64")
        self.grid_size = grid_size
        self.traveled_path = [tuple(self.current_position)]
        self.look_ahead_distance = look_ahead_distance
        self.current_index = 0
        self.current_heading = initial_heading  # Initialize the current heading
        self.commands = []

    def move_along_path(self, speed=1.0, pause=0.1):
        """
        Simulates the rover moving along the path.
        """
        print("Starting path following...")
        for waypoint in self.path:
            direction = np.array(waypoint, dtype="float64") - self.current_position
            distance = np.linalg.norm(direction)

            if distance > 0:
                step = direction / distance * speed

                while np.linalg.norm(direction) > np.linalg.norm(step):
                    self.current_position += step
                    self.traveled_path.append(tuple(np.round(self.current_position).astype(int)))
                    direction = np.array(waypoint, dtype="float64") - self.current_position
                    self.visualize()
                    time.sleep(pause)

                self.current_position = np.array(waypoint, dtype="float64")
                self.traveled_path.append(tuple(waypoint))
                self.visualize()
                time.sleep(pause)

        print("Path following complete.")

    def visualize(self, obstacles=None):
        """
        Visualizes the path, the current position of the rover, and obstacles.

        Parameters:
        - obstacles (list of tuples): List of obstacle coordinates to plot.
        """
        plt.clf()
        center_x, center_y = self.current_position
        plt.xlim(center_x - 10, center_x + 10)
        plt.ylim(center_y - 10, center_y + 10)
        plt.grid(True)

        # Plot the path
        x, y = zip(*self.path)
        plt.plot(x, y, linestyle="--", color="gray", label="Path")

        # Plot traveled path
        if self.traveled_path:
            tx, ty = zip(*self.traveled_path)
            plt.plot(tx, ty, color="blue", label="Traveled Path")

        # Plot current position
        plt.plot(self.current_position[0], self.current_position[1], "ro", label="Rover")

        # Plot obstacles
        if obstacles:
            ox, oy = zip(*obstacles)
            plt.scatter(ox, oy, color="red", label="Obstacles")

        plt.legend()
        plt.pause(0.01)
 
    def pure_pursuit(self):
        """
        Locate the next look-ahead point on the path.
        """
        for i in range(self.current_index, len(self.path)):
            point = np.array(self.path[i], dtype="float64")
            distance = np.linalg.norm(point - self.current_position)
            if distance >= self.look_ahead_distance:
                self.current_index = i
                return point
        return np.array(self.path[-1], dtype="float64")  # Final point if no valid look-ahead

    def move_with_pure_pursuit(self, speed=1.0, pause=0.1):
        """
        Follow the path using Pure Pursuit.
        """
        print("Following path with Pure Pursuit...")
        while self.current_index < len(self.path) - 1:
            target_point = self.pure_pursuit()
            direction = target_point - self.current_position
            distance = np.linalg.norm(direction)

            if distance > 0:
                step = direction / distance * speed
                self.current_position += step
                self.traveled_path.append(tuple(self.current_position))
                self.visualize()
                time.sleep(pause)

        print("Path following complete.")

    def move_with_pure_pursuit_obstacle_avoidance(
        self, speed=1.0, pause=0.1, obstacle_positions=None, detection_radius=1.5, replan_function=None, grid_size=(50, 50)
    ):
        """
        Moves the rover along the path using the pure pursuit algorithm with obstacle avoidance.

        Parameters:
        - speed (float): Movement speed.
        - pause (float): Pause between updates (for visualization).
        - obstacle_positions (list of tuples): List of obstacle coordinates.
        - detection_radius (float): Radius to detect obstacles.
        - replan_function (callable): Function to replan path. Takes (current_position, target, obstacles, grid_size).
        - grid_size (tuple): The size of the grid as (width, height).

        Returns:
        - None
        """
        print("Starting pure pursuit with obstacle avoidance...")

        for waypoint in self.path:
            while True:
                # Check for obstacles
                if obstacle_positions and self.obstacle_detected(obstacle_positions, detection_radius):
                    print(f"Obstacle detected near {self.current_position}. Replanning...")
                    self.visualize(obstacles=obstacle_positions)  # Visualize obstacles dynamically

                    if replan_function:
                        new_path = replan_function(
                            tuple(self.current_position), waypoint, obstacle_positions, grid_size
                        )
                        if new_path:
                            print(f"Replanned path: {new_path}")
                            self.path = new_path + self.path[self.path.index(waypoint) + 1:]
                            break  # Replan for current waypoint
                        else:
                            print(f"Failed to replan from {self.current_position} to {waypoint}. Trying next waypoint...")
                            break  # Skip current waypoint if replanning fails

                # Move towards waypoint
                direction = np.array(waypoint) - self.current_position
                distance = np.linalg.norm(direction)

                if distance <= self.look_ahead_distance:
                    print(f"Waypoint {waypoint} reached.")
                    break  # Reached the waypoint

                step = direction / distance * speed
                self.current_position += step
                self.traveled_path.append(tuple(self.current_position))
                self.visualize(obstacles=obstacle_positions)
                time.sleep(pause)

        print("Path following with obstacle avoidance complete.")
        
    def move_with_pure_pursuit_and_commands(self, speed=1.0, pause=0.1):
        """
        Move along the path using Pure Pursuit while emitting commands.
        """
        print("Starting Pure Pursuit with command output...")
        for waypoint in self.path:
            direction = np.array(waypoint) - self.current_position
            distance = np.linalg.norm(direction)
            
            if distance > 0:
                step = direction / distance * speed

                while np.linalg.norm(direction) > np.linalg.norm(step):
                    self.current_position += step
                    command = f"Move forward by {np.linalg.norm(step):.2f} meters"
                    print(command)
                    self.visualize()
                    time.sleep(pause)
                    direction = np.array(waypoint) - self.current_position

                turn_angle = np.degrees(np.arctan2(direction[1], direction[0]))
                print(f"Turn to heading {turn_angle:.2f}°")
                self.current_position = np.array(waypoint)
                self.visualize()

        print("Path following with commands complete.")

    def generate_and_execute_commands(self):
        """
        Generate movement commands for the path and simulate execution.
        """
        self.commands = calculate_commands(tuple(self.current_position), self.current_heading, self.path[1:])
        print("Generated Commands:")
        for command, value in self.commands:
            print(f"{command} {value:.2f}")

        self.execute_commands()

    def execute_commands(self):
        """
        Simulate the execution of movement commands.
        """
        print("Executing commands")
        for command, value in self.commands:
            if command == Command.FORWARD:
                self.move_forward(value)
            elif command == Command.TURN_LEFT:
                self.turn(value)
            elif command == Command.TURN_RIGHT:
                self.turn(-value)
            elif command == Command.STOP:
                print("Rover stopped.")

    def move_forward(self, distance):
        direction = np.array([math.cos(self.current_heading), math.sin(self.current_heading)])
        steps = int(distance)
        for _ in range(steps):
            self.current_position += direction
            self.traveled_path.append(tuple(self.current_position))
            self.visualize()

    def turn(self, angle):
        self.current_heading = (self.current_heading + angle) % (2 * math.pi)

    def check_for_resource(self):
        """
        Simulate resource detection (placeholder for actual detection logic).
        """
        # Example condition for detecting a resource
        if np.random.random() < 0.1:  # 10% chance per step
            print("Resource detected! Stopping search.")
            return True
        return False

    def move_with_resource_check(self, speed=1.0, pause=0.1):
        """
        Move along the path and stop if a resource is detected.
        """
        print("Starting Pure Pursuit with resource check...")
        for waypoint in self.path:
            direction = np.array(waypoint) - self.current_position
            distance = np.linalg.norm(direction)

            while distance > 0:
                if self.check_for_resource():
                    return
                step = direction / distance * speed
                self.current_position += step
                self.visualize()
                time.sleep(pause)
                direction = np.array(waypoint) - self.current_position
                distance = np.linalg.norm(direction)
        print("Path following complete.")    

    def obstacle_detected(self, obstacle_positions, detection_radius=1.0):
        """
        Checks if there is an obstacle within the detection radius of the rover's current position.

        Parameters:
        - obstacle_positions (list of tuples): List of (x, y) coordinates of obstacles.
        - detection_radius (float): Radius within which obstacles are considered detected.

        Returns:
        - bool: True if an obstacle is detected, False otherwise.
        """
        for obstacle in obstacle_positions:
            distance = np.linalg.norm(np.array(obstacle) - self.current_position)
            if distance <= detection_radius:
                print(f"Obstacle detected at {obstacle}, distance: {distance:.2f}")
                return True
        return False    

def test_path_follower_with_commands():
    """
    Test the PathFollower with command generation and execution.
    """
    expanding_square_path = generate_expanding_square(center=(0, 0), distance=5, max_side_length=6)

    follower = PathFollower(expanding_square_path)
    plt.ion()
    plt.figure(figsize=(10, 10))
    follower.visualize()

    follower.generate_and_execute_commands()
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    test_path_follower_with_commands()

def test_path_follower():
    """
    Test the PathFollower with sine wave and expanding square paths.
    """
    # Generate paths
    sine_wave_path = generate_sine_wave(amplitude=10, wavelength=20, num_points=500)
    expanding_square_path = generate_expanding_square(center=(0, 0), distance=5, max_side_length=6)

    # Choose the path to test (uncomment one of the lines below)
    # path = sine_wave_path
    path = expanding_square_path

    # Create the PathFollower
    follower = PathFollower(path)

    # Visualize initial state
    plt.ion()
    plt.figure(figsize=(10, 10))
    follower.visualize()

    # Start path following
    follower.move_along_path(speed=0.5, pause=0.1)
    plt.ioff()
    plt.show()
