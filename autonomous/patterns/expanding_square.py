# patterns/expanding_square.py

import matplotlib.pyplot as plt

def generate_expanding_square_pattern(center=(0, 0), steps=5):
    """
    Generate an expanding square pattern.
    
    Parameters:
        center (tuple): The center of the pattern (x, y).
        steps (int): The number of steps to expand the square.

    Returns:
        list: A list of (x, y) tuples representing the pattern.
    """
    x, y = center
    pattern = []
    length = 1  # Initial step length

    for _ in range(steps):
        # Move right
        for _ in range(length):
            x += 1
            pattern.append((x, y))
        # Move up
        for _ in range(length):
            y += 1
            pattern.append((x, y))
        length += 1  # Increment length after two directions
        # Move left
        for _ in range(length):
            x -= 1
            pattern.append((x, y))
        # Move down
        for _ in range(length):
            y -= 1
            pattern.append((x, y))
        length += 1  # Increment length for the next square

    return pattern

def visualize_expanding_square_pattern(center=(0, 0), steps=5):
    """
    Visualize an expanding square pattern using matplotlib.
    
    Parameters:
        center (tuple): The center of the pattern (x, y).
        steps (int): The number of steps to expand the square.
    """
    pattern = generate_expanding_square_pattern(center, steps)
    x, y = zip(*pattern)

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, linestyle='-', marker='o', color='blue')
    plt.title(f"Expanding Square Pattern (Steps: {steps})")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    # Example usage
    visualize_expanding_square_pattern(center=(0, 0), steps=10)