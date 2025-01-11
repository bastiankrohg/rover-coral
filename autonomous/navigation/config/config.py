# config.py

# Calibration Constants
REAL_WORLD_SCALE = 0.1  # Scale factor for converting track distance to real-world distance (meters/grid unit)
ROVER_SPEED = 0.5       # Nominal speed of the rover (meters/second)
TURN_RADIUS = 0.5       # Turning radius of the rover (meters)

# Search Pattern Parameters
EXPANDING_SQUARE_DISTANCE = 5  # Distance (grid units) for each segment of the expanding square
MAX_SQUARE_SIDE_LENGTH = 6     # Maximum side length of the square in multiples of distance

# Sine Wave Parameters
SINE_WAVE_AMPLITUDE = 10       # Amplitude of the sine wave
SINE_WAVE_WAVELENGTH = 20      # Wavelength of the sine wave
SINE_WAVE_NUM_POINTS = 500     # Number of points in the sine wave

# Visualization Settings
GRID_SIZE = (50, 50)  # Size of the visualization grid