# algorithms/a_star.py

import heapq
import math

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