# main.py

from environment.environment import Environment
from navigation.rover import Rover
from visualization.plotter import Visualizer
from algorithms.a_star import a_star
import time

def main():
    # Initialize the environment
    grid_size = (20, 20)
    obstacles = [(5, 5), (5, 6), (5, 7), (10, 10), (10, 11), (10, 12)]
    resources = [(3, 3), (15, 15)]  # Resource points
    start_position = (0, 0)
    max_distance = 500.0  # Maximum travel distance for the rover

    env = Environment(grid_size, obstacles, resources, start_position)

    # Initialize the rover
    rover = Rover(
        start_position=start_position,
        grid_size=grid_size,
        obstacles=obstacles,
        resources=resources,
        size=1.0,            # Rover size
        nominal_speed=1.0,   # Nominal speed
        turn_radius=1.0,     # Turn radius
        turning_speed=0.1    # Turning speed (radians per time step)
    )

    # Initialize the visualization
    visualizer = Visualizer(grid_size, obstacles, resources)

    # Simulation loop
    try:
        while rover.total_distance_traveled < max_distance:
            # Update visualization
            visualizer.update(rover, rover.optimal_path)

            # Perform a 360-degree scan
            detected_resources = rover.perform_360_scan()
            if detected_resources:
                # Register all detected resources
                for resource in detected_resources:
                    if resource not in rover.resource_registry:
                        rover.resource_registry.add(resource)
                        print(f"Resource registered: {resource}")

                # Navigate to the closest resource
                target = tuple(detected_resources[0])  # Closest resource
                rover.optimal_path = a_star(tuple(rover.position), target, obstacles, grid_size)
                if rover.navigate_to(target, rover.optimal_path):
                    # Remove the resource from the environment
                    env.remove_resource(target)
                    print(f"Resource at {target} collected!")
            else:
                # Perform expanding square search
                rover.search_area()

            time.sleep(0.1)  # Adjust loop speed as necessary

        # End of simulation
        print("Search complete.")
        print(f"Resources found: {rover.resource_registry}")
        print(f"Total distance traveled: {rover.total_distance_traveled:.2f}")
        visualizer.display_final()

    except KeyboardInterrupt:
        print("Simulation terminated by user.")
        visualizer.display_final()

if __name__ == "__main__":
    main()