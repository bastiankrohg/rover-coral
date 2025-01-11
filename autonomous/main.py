from navigation.rover import Rover
from navigation.path_generator import generate_expanding_square_waypoints
from visualization.plotter import Visualizer
from navigation.config.config import (
    GRID_SIZE,
    EXPANDING_SQUARE_DISTANCE,
    MAX_SQUARE_SIDE_LENGTH,
    REAL_WORLD_SCALE
)


def main():
    """
    Main function to simulate the rover's autonomous navigation using waypoints.
    """
    # Define environment settings
    grid_size = GRID_SIZE
    obstacles = [(5, 5), (5, 6), (6, 5), (10, 10), (10, 11), (11, 10)]  # Some obstacles
    resources = [(15, 15), (18, 18)]  # Resource positions
    start_position = (0, 0)  # Starting position of the rover

    # Initialize the rover
    rover = Rover(
        start_position=start_position,
        grid_size=grid_size,
        obstacles=obstacles,
        resources=resources,
        size=1.0,            # Rover size (in grid units)
        nominal_speed=0.5,   # Nominal speed
        turn_radius=0.5,     # Turning radius
        turning_speed=0.1    # Turning speed (radians per step)
    )

    # Initialize the visualizer
    visualizer = Visualizer(grid_size, obstacles, resources)

    # Generate waypoints for the expanding square search pattern, excluding the starting position
    waypoints = generate_expanding_square_waypoints(
        center=start_position,
        distance=EXPANDING_SQUARE_DISTANCE,
        max_side_length=MAX_SQUARE_SIDE_LENGTH
    )[1:]  # Skip the first waypoint (initial position)
    print(f"Generated waypoints: {waypoints}")

    # Simulate navigation
    try:
        # Add a threshold for waypoint completion
        threshold = 1.0  # Waypoint completion threshold in grid units
        rover.navigate_to_waypoints(waypoints, threshold=threshold)

        # Display final results
        print("Waypoint navigation complete.")
        print(f"Total distance traveled: {rover.total_distance_traveled:.2f} meters (scaled by {REAL_WORLD_SCALE}).")
        visualizer.display_final()

    except KeyboardInterrupt:
        print("Simulation interrupted by user.")
        visualizer.display_final()


if __name__ == "__main__":
    main()