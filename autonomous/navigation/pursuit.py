from path_generator import (
    generate_expanding_square, 
    generate_sine_wave, 
    smooth_path_with_bezier
)
from path_follower import PathFollower
from movement_commands import generate_movement_commands
from dynamic_obstacle_handler import recalculate_path
from algorithms.a_star import a_star

def replan_path(current_position, target, obstacles, grid_size=(50, 50)):
    """
    Replan path using A* algorithm.

    Parameters:
    - current_position: Current position of the rover.
    - target: Target waypoint.
    - obstacles: List of obstacle coordinates.
    - grid_size: Grid size (width, height).

    Returns:
    - List of tuples: New path or an empty list if no path is found.
    """
    print(f"Replanning from {current_position} to {target}...")
    
    # Generate a new path
    new_path = a_star(current_position, target, obstacles, grid_size)
    
    if not new_path:
        print(f"Failed to replan from {current_position} to {target}. Trying next waypoint...")
        return []  # Return an empty list if no path is found

    print(f"New path: {new_path}")
    return new_path

def test_workflow(use_bezier=False, generate_commands=True):
    """
    Test workflow for path generation, optional smoothing, path following, 
    and movement command generation.
    
    Parameters:
    - use_bezier (bool): Whether to smooth the path using Bezier curves.
    - generate_commands (bool): Whether to generate and print movement commands.
    """
    # Step 1: Generate Waypoints
    waypoints = generate_expanding_square(center=(0, 0), distance=5, max_side_length=6)

    # Step 2: Optionally Smooth Path
    if use_bezier:
        smoothed_path = smooth_path_with_bezier(waypoints, num_points=200)
        print("Using bezier-smoothed path.")
    else:
        smoothed_path = waypoints
        print("Using original waypoints.")

    # Step 3: Pure Pursuit Path Following
    print("\nStarting path following...")
    follower = PathFollower(smoothed_path, look_ahead_distance=2.0)
    follower.move_with_pure_pursuit(speed=1.0, pause=0.1)
    print("Path following complete.")

    # Step 4: Generate Movement Commands
    if generate_commands:
        print("\nGenerating movement commands...")
        commands = generate_movement_commands(smoothed_path)
        print("Movement Commands:")
        for i, (heading, speed) in enumerate(commands):
            try:
                heading = float(heading)
                speed = float(speed)
                print(f"Step {i + 1}: Heading = {heading:.2f}, Speed = {speed:.2f}")
            except ValueError:
                print(f"Step {i + 1}: Invalid command - Heading: {heading}, Speed: {speed}")
                
def test_workflow_with_obstacle_avoidance(use_bezier=False, generate_commands=True):
    """
    Test workflow with obstacle avoidance.
    """
    # Step 1: Generate Waypoints
    waypoints = generate_expanding_square(center=(0, 0), distance=5, max_side_length=6)

    # Step 2: Optionally Smooth Path
    smoothed_path = smooth_path_with_bezier(waypoints, num_points=200) if use_bezier else waypoints
    print("Using bezier-smoothed path." if use_bezier else "Using original waypoints.")

    # Step 3: Define Obstacles
    obstacle_positions = [(10, 10), (12, 8), (8, 12)]

    # Step 4: Path Following with Obstacle Avoidance
    print("\nStarting path following with obstacle avoidance...")
    follower = PathFollower(smoothed_path, look_ahead_distance=2.0)
    follower.move_with_pure_pursuit_obstacle_avoidance(
        speed=1.0,
        pause=0.1,
        obstacle_positions=obstacle_positions,
        detection_radius=2.0,
        replan_function=replan_path
    )

    # Step 5: Generate Movement Commands
    if generate_commands:
        print("\nGenerating movement commands...")
        commands = generate_movement_commands(follower.traveled_path)
        print("Movement Commands:")
        for i, (heading, speed) in enumerate(commands):
            print(f"Step {i + 1}: Heading = {heading:.2f}, Speed = {speed:.2f}")

if __name__ == "__main__":
    # Example: Run workflow with and without bezier smoothing
    #print("Running without bezier smoothing:")
    
    #test_workflow(use_bezier=False, generate_commands=True)
    #test_workflow_with_obstacle_avoidance(use_bezier=False, generate_commands=True)

    #print("\nRunning with bezier smoothing:")
    #test_workflow_with_obstacle_avoidance(use_bezier=True, generate_commands=True)

    print("\nRunning without bezier smoothing:")
    test_workflow_with_obstacle_avoidance(use_bezier=False, generate_commands=True)