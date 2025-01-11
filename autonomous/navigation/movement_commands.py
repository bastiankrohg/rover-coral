import numpy as np

def generate_movement_commands(path, nominal_speed=1.0):
    """
    Generate movement commands (heading, speed) from the path.

    Parameters:
    - path: List of (x, y) points representing the path.
    - nominal_speed: Speed for each segment.

    Returns:
    - List of (heading, speed) tuples.
    """
    commands = []
    for i in range(1, len(path)):
        direction = np.array(path[i]) - np.array(path[i - 1])
        heading = np.arctan2(direction[1], direction[0])
        commands.append((heading, nominal_speed))
    return commands