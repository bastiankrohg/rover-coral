from environment.environment import Environment
from navigation.rover import Rover
from visualization.plotter import Visualizer
from algorithms.a_star import a_star
import time

from navigation.config.config import (
    REAL_WORLD_SCALE,
    EXPANDING_SQUARE_DISTANCE,
    MAX_SQUARE_SIDE_LENGTH,
    SINE_WAVE_AMPLITUDE,
    SINE_WAVE_WAVELENGTH,
    SINE_WAVE_NUM_POINTS
)

def main():
    # Initialize the environment
    grid_size = (50, 50)
    obstacles = [(5, 5), (5, 6), (5, 7), (10, 10), (10, 11), (10, 12)]
    resources = [(3, 3), (15, 15)]  # Resource points
    start_position = (0, 0)
    max_distance = 200.0

    env = Environment(grid_size, obstacles, resources, start_position)
    rover = Rover(
        start_position=start_position,
        grid_size=grid_size,
        obstacles=obstacles,
        resources=resources,
    )
    visualizer = Visualizer(grid_size, obstacles, resources)

    # Initialize the visualization plot
    visualizer.initialize_plot()


    # Report initial state
    rover.report_state()

    try:
        while rover.total_distance_traveled < max_distance:
            # Perform a 360-degree scan
            detected_resources = rover.perform_360_scan()

            if detected_resources:
                # Navigate to each detected resource
                for resource in detected_resources:
                    rover.navigate_to_resource(resource)

            else:
                # Explore the area using a search pattern
                rover.explore()

            # Update visualization
            visualizer.update(rover.position, rover.traveled_path)

            time.sleep(0.1)  # Simulate real-time behavior

        print("Mission complete.")
        print(f"Verified resources: {rover.verified_resources}")
        visualizer.display_final()

    except KeyboardInterrupt:
        print("Simulation terminated by user.")
        visualizer.display_final()


if __name__ == "__main__":
    main()