import matplotlib.pyplot as plt
import numpy as np
import heapq
import time
import math

# Define the environment
grid_size = (20, 20)
obstacles = [(5, 5), (5, 6), (5, 7), (10, 10), (10, 11), (10, 12)]
resources = [(15, 15)]
start = (0, 0)
goal = (19, 19)

# A* Algorithm Implementation with Diagonal Movements
def heuristic(a, b):
    # Diagonal distance heuristic
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy)

def a_star(start, goal, obstacles, grid_size):
    # Define possible movements: 8 directions (vertical, horizontal, diagonal)
    neighbors = [
        (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal directions
        (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
    ]
    # Movement costs: 1 for cardinal, sqrt(2) for diagonal
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
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            return data[::-1]  # Return reversed path

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + move_cost[(i, j)]
            if 0 <= neighbor[0] < grid_size[0] and 0 <= neighbor[1] < grid_size[1]:
                if neighbor in obstacles:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, float('inf')):
                continue

            if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return []

# Visualization with Blitting
def plot_environment_with_blit(path):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, grid_size[0])
    ax.set_ylim(0, grid_size[1])

    # Plot obstacles
    for obs in obstacles:
        ax.add_patch(plt.Rectangle(obs, 1, 1, color='black'))

    # Plot resources
    for res in resources:
        ax.add_patch(plt.Rectangle(res, 1, 1, color='green'))

    # Plot start and goal
    ax.add_patch(plt.Rectangle(start, 1, 1, color='blue'))
    ax.add_patch(plt.Rectangle(goal, 1, 1, color='red'))

    # Initialize rover position
    rover, = ax.plot([], [], 'ro', markersize=8)  # 'ro' for red circle

    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)

    # Draw the canvas once, background will be reused
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(fig.bbox)

    # Animation loop
    for position in path:
        # Restore the background
        fig.canvas.restore_region(background)

        # Update rover position
        rover.set_data([position[0] + 0.5], [position[1] + 0.5])  # Center in the grid cell

        # Redraw only the rover
        ax.draw_artist(rover)

        # Blit the updated area
        fig.canvas.blit(fig.bbox)

        # Pause to control the animation speed
        plt.pause(0.1)

    # Keep the final plot displayed
    plt.show()

# Main Autonomous Navigation Function
def autonomous_navigation():
    # Compute path using A*
    path = a_star(start, goal, obstacles, grid_size)

    # Simulate rover movement along the path with visualization
    if path:
        plot_environment_with_blit(path)
    else:
        print("No path found to the goal.")

if __name__ == "__main__":
    autonomous_navigation()