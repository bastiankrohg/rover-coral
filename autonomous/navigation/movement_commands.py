import numpy as np
import math
from commands import Command

def generate_movement_commands(path):
    """
    Generate movement commands (heading and speed) for the given path.
    """
    commands = []
    for i in range(len(path) - 1):
        start = np.array(path[i])
        end = np.array(path[i + 1])
        direction = end - start
        distance = np.linalg.norm(direction)
        if distance == 0:
            continue  # Skip if the rover is already at the target

        heading = np.arctan2(direction[1], direction[0])
        speed = 1.0  # Example constant speed

        # Validate outputs
        if isinstance(heading, (int, float)) and isinstance(speed, (int, float)):
            commands.append((heading, speed))
        else:
            print(f"Invalid command: heading={heading}, speed={speed}")

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