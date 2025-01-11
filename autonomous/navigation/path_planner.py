from algorithms.a_star import a_star, a_star_bis


def generate_paths_for_waypoints(waypoints, obstacles, grid_size):
    """
    Generate paths between sequential waypoints using A*.

    Parameters:
    - waypoints: List of (x, y) waypoints.
    - obstacles: List of (x, y) obstacle coordinates.
    - grid_size: Size of the grid as (width, height).

    Returns:
    - List of paths connecting the waypoints.
    """
    paths = []
    for i in range(len(waypoints) - 1):
        start = waypoints[i]
        goal = waypoints[i + 1]
        print(f"Generating path from {start} to {goal}...")

        #path = a_star(start, goal, obstacles, grid_size)
        path = a_star(start, goal, obstacles, grid_size)
        if not path:
            print(f"Path from {start} to {goal} is blocked. Skipping.")
            continue

        paths.append(path)

    return paths