# algorithms/a_star.py

import heapq
import math
import numpy as np

def heuristic(a, b):
    """Diagonal distance heuristic."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy)

def a_star(start, goal, obstacles, grid_size):
    """A* pathfinding algorithm with diagonal movements."""
    # Ensure start and goal are tuples
    start = tuple(start)
    goal = tuple(goal)
    obstacles = {tuple(obs) for obs in obstacles}  # Ensure obstacles are hashable

    neighbors = [
        (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal directions
        (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
    ]
    move_cost = {n: (math.sqrt(2) if abs(n[0]) + abs(n[1]) == 2 else 1) for n in neighbors}

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return reversed path

        close_set.add(current)
        for i, j in neighbors:
            neighbor = (current[0] + i, current[1] + j)
            tentative_g_score = gscore[current] + move_cost[(i, j)]

            if not (0 <= neighbor[0] < grid_size[0] and 0 <= neighbor[1] < grid_size[1]):
                continue  # Skip out-of-bounds neighbors

            if neighbor in obstacles:
                continue  # Skip obstacles

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, float('inf')):
                continue

            if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return []  # Return an empty list if no path is found

def a_star_bis(start, goal, obstacles, grid_size):
    """
    Enhanced A* algorithm to handle large grids and obstacles.
    """
    neighbors = [
        (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal directions
        (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
    ]

    def in_bounds(position):
        x, y = position
        return (
            grid_size[0][0] <= x <= grid_size[0][1] and
            grid_size[1][0] <= y <= grid_size[1][1]
        )

    def is_collision(position):
        return position in obstacles

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set = [(f_score[start], start)]
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)

            if not in_bounds(neighbor) or is_collision(neighbor):
                continue

            tentative_g_score = g_score[current] + heuristic(current, neighbor)
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    print(f"No path found from {start} to {goal}")
    return []

def a_star_occupancy(start, goal, occupancy_map, grid_size):
    """
    A* pathfinding algorithm using an occupancy map.

    Parameters:
    - start: Starting position as (x, y).
    - goal: Goal position as (x, y).
    - occupancy_map: 2D numpy array indicating free and occupied cells.
    - grid_size: ((x_min, x_max), (y_min, y_max)) tuple defining the grid.

    Returns:
    - List of (x, y) points representing the path, or an empty list if no path is found.
    """
    print(f"Starting A* from {start} to {goal}")

    neighbors = [
        (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal directions
        (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
    ]

    # Ensure start and goal are tuples of integers
    start = tuple(map(int, start))
    goal = tuple(map(int, goal))

    # Extract grid bounds
    x_min, x_max = grid_size[0]
    y_min, y_max = grid_size[1]

    # A* initialization
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        # Check if the goal is reached
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # Explore neighbors
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)

            # Check bounds
            if not (x_min <= neighbor[0] <= x_max and y_min <= neighbor[1] <= y_max):
                continue

            # Calculate map indices
            map_x = int(neighbor[0] - x_min)
            map_y = int(neighbor[1] - y_min)

            # Ensure valid indexing into the occupancy map
            if not (0 <= map_x < occupancy_map.shape[1] and 0 <= map_y < occupancy_map.shape[0]):
                continue

            # Check if the cell is occupied
            if occupancy_map[map_y, map_x] == 1:  # Note: (y, x) for numpy indexing
                continue

            # Compute tentative g-score
            tentative_g_score = g_score[current] + heuristic(current, neighbor)

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                # Update path
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

        #print(f"Open set: {open_set}")
        #print(f"Current position: {current}")

    print(f"No path found from {start} to {goal}")
    return []  # Return an empty path if no solution exists