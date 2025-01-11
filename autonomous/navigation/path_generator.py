import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

from config.config import (
    REAL_WORLD_SCALE,
    EXPANDING_SQUARE_DISTANCE,
    MAX_SQUARE_SIDE_LENGTH,
    SINE_WAVE_AMPLITUDE,
    SINE_WAVE_WAVELENGTH,
    SINE_WAVE_NUM_POINTS
)


def calculate_path_distance(path, scale=1.0):
    """
    Calculate the total distance of a path.

    Parameters:
    - path: List of (x, y) points representing the path
    - scale: Scaling factor to adjust the distance to real-world units

    Returns:
    - Total distance of the path
    """
    total_distance = 0
    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]
        total_distance += np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return total_distance * scale  # Apply scaling factor for real-world units


def generate_sine_wave(amplitude=SINE_WAVE_AMPLITUDE, wavelength=SINE_WAVE_WAVELENGTH, num_points=SINE_WAVE_NUM_POINTS, plot=False):
    """
    Generate a smoother sine wave path.

    Parameters:
    - amplitude: Height of the wave
    - wavelength: Distance between wave peaks
    - num_points: Number of points in the sine wave
    - plot: If True, plot the path using matplotlib

    Returns:
    - List of (x, y) points representing the sine wave
    """
    x = np.linspace(0, wavelength * 5, num=num_points)  # Length is 5 wavelengths
    y = amplitude * np.sin(2 * np.pi * x / wavelength)
    path = list(zip(x, y))

    if plot:
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, label="Sine Wave", color="blue")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Sine Wave Path")
        plt.grid(True)
        plt.legend()
        plt.show()

    return path


def generate_expanding_square(center=(0, 0), distance=EXPANDING_SQUARE_DISTANCE, max_side_length=MAX_SQUARE_SIDE_LENGTH, plot=False):
    """
    Generate an expanding square path starting from the center.

    Parameters:
    - center: The (x, y) center of the square
    - distance: Distance moved in each straight line segment
    - max_side_length: Maximum length of the square sides in multiples of 'distance'
    - plot: If True, plot the path using matplotlib

    Returns:
    - List of (x, y) points representing the expanding square path
    """
    x, y = center
    path = [(x, y)]
    current_length = 1  # Current length of square sides in 'distance' units

    while current_length <= max_side_length:
        # Move right
        for _ in range(current_length):
            x += distance
            path.append((x, y))

        # Move up
        for _ in range(current_length):
            y += distance
            path.append((x, y))

        current_length += 1

        # Move left
        for _ in range(current_length):
            x -= distance
            path.append((x, y))

        # Move down
        for _ in range(current_length):
            y -= distance
            path.append((x, y))

        current_length += 1

    if plot:
        px, py = zip(*path)
        plt.figure(figsize=(10, 10))
        plt.plot(px, py, label="Expanding Square", marker="o", linestyle="--", color="green")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Expanding Square Path")
        plt.grid(True)
        plt.legend()
        plt.show()

    return path

def generate_expanding_square_waypoints(center, distance=5, max_side_length=6):
    """
    Generate waypoints for an expanding square pattern starting from the given center.

    Parameters:
    - center: The (x, y) starting point of the square.
    - distance: Distance moved in each straight line segment.
    - max_side_length: Maximum length of the square sides in multiples of 'distance'.

    Returns:
    - List of waypoints for the expanding square.
    """
    x, y = center
    waypoints = []
    current_length = 1

    while current_length <= max_side_length:
        # Right
        for _ in range(current_length):
            x += distance
        waypoints.append((x, y))

        # Up
        for _ in range(current_length):
            y += distance
        waypoints.append((x, y))

        current_length += 1

        # Left
        for _ in range(current_length):
            x -= distance
        waypoints.append((x, y))

        # Down
        for _ in range(current_length):
            y -= distance
        waypoints.append((x, y))

        current_length += 1

    return waypoints


def test_path_generators():
    """
    Test the path generators and print the total distances.

    This function tests both the sine wave and expanding square generators,
    calculates the total distance of each path, and optionally plots them.
    """
    # Test sine wave generator
    print("Testing Sine Wave Generator...")
    sine_wave = generate_sine_wave(plot=True)
    total_distance = calculate_path_distance(sine_wave, scale=REAL_WORLD_SCALE)
    print(f"Total distance of sine wave: {total_distance:.2f} meters")

    # Test expanding square generator
    print("\nTesting Expanding Square Generator...")
    expanding_square = generate_expanding_square(plot=True)
    total_distance = calculate_path_distance(expanding_square, scale=REAL_WORLD_SCALE)
    print(f"Total distance of expanding square: {total_distance:.2f} meters")

def smooth_path_with_bezier(waypoints, num_points=100):
    """
    Smooth the given waypoints using Bezier curves.

    Parameters:
    - waypoints: List of (x, y) waypoints.
    - num_points: Number of interpolated points for the smooth path.

    Returns:
    - List of (x, y) tuples representing the smoothed path.
    """
    waypoints = np.array(waypoints)
    tck, _ = splprep([waypoints[:, 0], waypoints[:, 1]], s=0)
    u = np.linspace(0, 1, num_points)
    smooth_path = splev(u, tck)
    return list(zip(smooth_path[0], smooth_path[1]))

if __name__ == "__main__":
    test_path_generators()