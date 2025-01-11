import matplotlib.pyplot as plt
from navigation.path_generator import generate_expanding_square_waypoints
from navigation.config.config import (
    EXPANDING_SQUARE_DISTANCE,
    MAX_SQUARE_SIDE_LENGTH,
)

# Define dummy obstacles and starting point for visualization
obstacles = [(5, 5), (5, 6), (6, 5), (10, 10), (10, 11), (11, 10)]
start_position = (0, 0)


def visualize_waypoints():
    """
    Generate and plot waypoints with dummy obstacles for verification.
    """
    # Generate waypoints
    waypoints = generate_expanding_square_waypoints(
        center=start_position,
        distance=EXPANDING_SQUARE_DISTANCE,
        max_side_length=MAX_SQUARE_SIDE_LENGTH
    )

    # Plot the waypoints
    plt.figure(figsize=(10, 10))
    plt.title("Generated Waypoints and Obstacles")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)

    # Plot obstacles
    for obs in obstacles:
        plt.scatter(*obs, c="red", label="Obstacle" if obs == obstacles[0] else "")

    # Plot waypoints
    waypoints_x, waypoints_y = zip(*waypoints)
    plt.plot(waypoints_x, waypoints_y, label="Waypoints", linestyle="--", marker="o", color="blue")

    # Starting point
    plt.scatter(*start_position, c="green", label="Start Position")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    visualize_waypoints()