from path_generator import (
    generate_expanding_square, 
    generate_sine_wave, 
    smooth_path_with_bezier
)
from path_follower import PathFollower
from algorithms.a_star import a_star
from movement_commands import generate_movement_commands

def test_workflow():
    # Step 1: Generate Waypoints
    waypoints = generate_expanding_square(center=(0, 0), distance=5, max_side_length=6)

    # Step 2: Smooth Path
    smoothed_path = smooth_path_with_bezier(waypoints, num_points=200)

    # Step 3: Pure Pursuit Path Following
    follower = PathFollower(smoothed_path, look_ahead_distance=2.0)
    follower.move_with_pure_pursuit(speed=1.0, pause=0.1)

    # Step 4: Generate Movement Commands
    commands = generate_movement_commands(smoothed_path)
    print("Movement Commands:")
    for heading, speed in commands:
        print(f"Heading: {heading:.2f}, Speed: {speed:.2f}")

if __name__ == "__main__":
    test_workflow()