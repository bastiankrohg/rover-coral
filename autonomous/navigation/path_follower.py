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

    def visualize(self):
        """
        Visualizes the path and the current position of the rover.
        """
        plt.clf()
        plt.xlim(-self.grid_size[0] // 2, self.grid_size[0] // 2)
        plt.ylim(-self.grid_size[1] // 2, self.grid_size[1] // 2)
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
