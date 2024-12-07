from pynput.keyboard import Listener, Key
import time
import threading
from coral_control import Coral

# Initialize Coral for gRPC communication
coral = Coral()

# Track pressed keys
pressed_keys = set()
stop_loop = False  # Flag to stop the continuous processing loop

def handle_combined_keys():
    """Handle simultaneous key presses to send appropriate gRPC commands."""
    if "w" in pressed_keys and "d" in pressed_keys:  # Forward + Turn Right
        coral.turn_right(angle=5)
        coral.drive_forward(speed=50)
    elif "w" in pressed_keys and "a" in pressed_keys:  # Forward + Turn Left
        coral.turn_left(angle=5)
        coral.drive_forward(speed=50)
    elif "s" in pressed_keys and "d" in pressed_keys:  # Reverse + Turn Right
        coral.turn_right(angle=5)
        coral.reverse(speed=50)
    elif "s" in pressed_keys and "a" in pressed_keys:  # Reverse + Turn Left
        coral.turn_left(angle=5)
        coral.reverse(speed=50)
    else:
        # Handle individual movement keys
        if "w" in pressed_keys:
            coral.drive_forward(speed=50)
        if "s" in pressed_keys:
            coral.reverse(speed=50)
        if "a" in pressed_keys:
            coral.rotate_on_spot(angle=-15)
        if "d" in pressed_keys:
            coral.rotate_on_spot(angle=15)

def on_press(key):
    """Handle key press events."""
    global stop_loop

    try:
        # Handle alphanumeric keys
        if hasattr(key, 'char') and key.char:
            pressed_keys.add(key.char.lower())
        elif key in (Key.tab, Key.space, Key.esc):
            pressed_keys.add(key)

        # Specific actions for non-char keys
        if key == Key.tab:
            print("Toggling resource list display.")
        elif key == Key.space:
            print("Toggling obstacle list display.")
        elif key == Key.esc:
            print("Exiting...")
            stop_loop = True
            return False  # Stop listener

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