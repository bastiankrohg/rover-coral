import numpy as np
import math
from commands import Command

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


def calculate_commands(current_position, current_heading, waypoints):
    """
    Generate movement commands to navigate through a series of waypoints.

    Parameters:
    - current_position: The rover's current position as (x, y).
    - current_heading: The rover's current heading in radians.
    - waypoints: List of (x, y) waypoints to follow.

    Returns:
    - List of commands as [(Command, angle_or_distance), ...].
    """
    commands = []
    position = current_position
    heading = current_heading

    for waypoint in waypoints:
        # Calculate direction to the waypoint
        direction = math.atan2(waypoint[1] - position[1], waypoint[0] - position[0])
        angle_diff = (direction - heading + math.pi) % (2 * math.pi) - math.pi

        # Add turn command if necessary
        if abs(angle_diff) > 1e-2:  # Allow slight tolerance
            if angle_diff > 0:
                commands.append((Command.TURN_LEFT, angle_diff))
            else:
                commands.append((Command.TURN_RIGHT, -angle_diff))

        # Update heading
        heading = direction

        # Calculate distance to the waypoint
        distance = math.sqrt((waypoint[0] - position[0]) ** 2 + (waypoint[1] - position[1]) ** 2)
        commands.append((Command.FORWARD, distance))

        # Update position
        position = waypoint

    # Add a stop command at the end
    commands.append((Command.STOP, 0))
    
    return commands