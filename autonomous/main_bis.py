# testing main with new occupancy method

from environment.environment import OccupancyEnvironment as Environment
from navigation.rover import Rover
from navigation.path_generator import generate_expanding_square_waypoints
from visualization.plotter import Visualizer
from algorithms.a_star import a_star_occupancy
from navigation.config.config import (
    GRID_SIZE,
    EXPANDING_SQUARE_DISTANCE,
    MAX_SQUARE_SIDE_LENGTH,
)

def main():
    """
    Main function to simulate the rover's autonomous navigation using waypoints and occupancy map.
    """
    # Define environment settings
    obstacles = [(5, 5), (5, 6), (6, 5), (10, 10), (10, 11), (11, 10)]  # Some obstacles
    resources = [(-5,-5), (15, 15), (18, 18)]  # Resource positions
    start_position = (0, 0)  # Starting position of the rover

    # Initialize the environment
    env = Environment(GRID_SIZE, obstacles, resources)

    # Initialize the rover
    rover = Rover(
        start_position=start_position,
        grid_size=GRID_SIZE,
        obstacles=obstacles,  # Pass as fallback
        resources=resources,
        size=1.0,
        nominal_speed=0.5,
        turn_radius=0.5,
        turning_speed=0.1
    )

    # Initialize the visualizer
    visualizer = Visualizer(GRID_SIZE, obstacles, resources)

    visualizer.initialize_plot()  # Cache the initial plot for blitting

    # Generate waypoints
    waypoints = generate_expanding_square_waypoints(
        center=start_position,
        distance=EXPANDING_SQUARE_DISTANCE,
        max_side_length=MAX_SQUARE_SIDE_LENGTH
    )
    print(f"Generated waypoints: {waypoints}")

    # Simulate navigation
    for waypoint in waypoints:
        print(f"Navigating to waypoint: {waypoint}")
        path = a_star_occupancy(rover.position, waypoint, env.occupancy_map, GRID_SIZE)

        if path:
            for step in path:
                rover.move_to(step)  # Update rover's position
                # Pass rover's position and traveled path to the visualizer
                visualizer.update(rover.position, rover.traveled_path)
        else:
            print(f"Unable to find a path to waypoint {waypoint}. Skipping.")

    print("Waypoint navigation complete.")

if __name__ == "__main__":
    main()