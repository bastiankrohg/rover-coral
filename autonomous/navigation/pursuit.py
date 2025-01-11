from path_generator import (
    generate_expanding_square, 
    generate_sine_wave, 
    smooth_path_with_bezier
)
from path_follower import PathFollower
from movement_commands import generate_movement_commands


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
            print(f"Step {i + 1}: Heading = {heading:.2f}, Speed = {speed:.2f}")


if __name__ == "__main__":
    # Example: Run workflow with and without bezier smoothing and with command generation
    print("Running without bezier smoothing:")
    test_workflow(use_bezier=False, generate_commands=True)

    print("\nRunning with bezier smoothing:")
    #test_workflow(use_bezier=True, generate_commands=True)