from algorithms.a_star import a_star

def recalculate_path(current_position, remaining_path, obstacles, grid_size):
    """
    Recalculate a path avoiding obstacles using A*.
    """
    if not remaining_path:
        return []

    new_path = []
    for waypoint in remaining_path:
        path = a_star(current_position, waypoint, obstacles, grid_size)
        if path:
            new_path.extend(path)
            current_position = waypoint
        else:
            print(f"Cannot reach waypoint {waypoint}, skipping.")
    return new_path