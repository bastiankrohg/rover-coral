from navigation.path_follower import PathFollower
from navigation.path_generator import generate_expanding_square_waypoints
from navigation.path_planner import generate_paths_for_waypoints
from navigation.config.config import (
    GRID_SIZE,
    EXPANDING_SQUARE_DISTANCE,
    MAX_SQUARE_SIDE_LENGTH,
)
from algorithms.a_star import a_star, a_star_bis
from visualization.plotter import Visualizer

def validate_waypoints(waypoints, obstacles):
    """
    Validate waypoints to ensure they are not within obstacles.
    """
    valid_waypoints = [wp for wp in waypoints if wp not in obstacles]
    if len(valid_waypoints) != len(waypoints):
        print("Some waypoints were adjusted or skipped due to obstacles.")
    return valid_waypoints

def test_path_generation_and_following():
    """
    Test generating paths with A* and following them using the path follower.
    """
    start_position = (0, 0)
    obstacles = [(5, 5), (5, 6), (6, 5), (10, 10), (10, 11), (11, 10)]

    # Generate waypoints
    waypoints = generate_expanding_square_waypoints(
        center=start_position,
        distance=EXPANDING_SQUARE_DISTANCE,
        max_side_length=MAX_SQUARE_SIDE_LENGTH,
    )

    waypoints = validate_waypoints(waypoints, obstacles)

    # Generate paths between waypoints
    paths = generate_paths_for_waypoints(waypoints, obstacles, GRID_SIZE)

    if not paths:
        print("No valid paths generated. Exiting test.")
        return

    # Initialize path follower and visualizer
    path_follower = PathFollower(paths[0])
    visualizer = Visualizer(GRID_SIZE, obstacles, [])

    # Simulate following the path
    for path in paths:
        path_follower.update_path(path)

        for _ in path:
            path_follower.move_along_path(speed=0.5, pause=0.1)
            visualizer.update(
                path_follower.current_position,
                path_follower.current_position,
            )

if __name__ == "__main__":
    test_path_generation_and_following()