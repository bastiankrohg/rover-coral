from pynput.keyboard import Listener, Key
import time
import threading
from coral_control import Coral

# Initialize Coral for gRPC communication
coral = Coral()

# Track pressed keys
pressed_keys = set()
stop_loop = False  # Flag to stop the continuous processing loop
resource_list_displayed = False  # Toggle state for resource list
obstacle_list_displayed = False  # Toggle state for obstacle list


def handle_combined_keys():
    """Handle simultaneous key presses to send appropriate gRPC commands."""
    if "w" in pressed_keys and "d" in pressed_keys:  # Forward + Turn Right
        coral.turn_right(angle=3)
        coral.drive_forward(speed=15)
    elif "w" in pressed_keys and "a" in pressed_keys:  # Forward + Turn Left
        coral.turn_left(angle=3)
        coral.drive_forward(speed=15)
    elif "s" in pressed_keys and "d" in pressed_keys:  # Reverse + Turn Right
        coral.turn_right(angle=3)
        coral.reverse(speed=15)
    elif "s" in pressed_keys and "a" in pressed_keys:  # Reverse + Turn Left
        coral.turn_left(angle=3)
        coral.reverse(speed=15)
    else:
        # Handle individual movement keys
        if "w" in pressed_keys:
            coral.drive_forward(speed=15)
        if "s" in pressed_keys:
            coral.reverse(speed=15)
        if "a" in pressed_keys:
            coral.turn_on_spot(angle=5)
        if "d" in pressed_keys:
            coral.turn_on_spot(angle=-5)


def on_press(key):
    """Handle key press events."""
    global stop_loop, resource_list_displayed, obstacle_list_displayed

    try:
        # Handle alphanumeric keys
        if hasattr(key, 'char') and key.char:
            pressed_keys.add(key.char.lower())
        elif key in (Key.tab, Key.space, Key.esc):
            pressed_keys.add(key)

        # Specific actions for non-char keys
        if key == Key.tab:
            resource_list_displayed = not resource_list_displayed
            print("Resource list display toggled:", resource_list_displayed)
        elif key == Key.space:
            obstacle_list_displayed = not obstacle_list_displayed
            print("Obstacle list display toggled:", obstacle_list_displayed)
        elif key == Key.esc:
            print("Exiting...")
            stop_loop = True
            return False  # Stop listener

        # Resource and obstacle placement
        if "o" in pressed_keys:
            coral.place_resource(distance=10)
        if "p" in pressed_keys:
            coral.place_obstacle(distance=10)

        # Handle simultaneous actions
        handle_combined_keys()

    except Exception as e:
        print(f"Error in on_press: {e}")


def on_release(key):
    """Handle key release events."""
    try:
        # Remove alphanumeric keys from the set
        if hasattr(key, 'char') and key.char:
            pressed_keys.discard(key.char.lower())
        elif key in (Key.tab, Key.space, Key.esc):
            pressed_keys.discard(key)

        # Stop all movement if no keys are pressed
        if not pressed_keys:
            coral.stop_movement()

    except Exception as e:
        print(f"Error in on_release: {e}")


def process_keys():
    """Continuously process key states for combined and individual actions."""
    global stop_loop

    while not stop_loop:
        if pressed_keys:
            handle_combined_keys()
        time.sleep(0.1)  # Process every 100ms to prevent high CPU usage


# Start listener thread
def start_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# Manage threads
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Start key processing
try:
    process_keys()
except KeyboardInterrupt:
    stop_loop = True
    listener_thread.join()
    print("Exiting...")