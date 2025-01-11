import matplotlib.pyplot as plt
import numpy as np
import time
from path_generator import generate_sine_wave, generate_expanding_square


class PathFollower:
    def __init__(self, path, grid_size=(50, 50)):
        self.path = path
        self.current_position = np.array(path[0], dtype="float64")
        self.grid_size = grid_size
        self.traveled_path = [tuple(self.current_position)]

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


if __name__ == "__main__":
    test_path_follower()