from pynput.keyboard import Listener, Key # type: ignore
import time
import threading
from coral_pi_map import Coral

# Initialize Coral for gRPC communication
coral = Coral()

# Track pressed keys
pressed_keys = set()
stop_loop = False  # Flag to stop the continuous processing loop
scanning_enabled = False

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
        if "q" in pressed_keys:  # Rotate mast left
            coral.rotate_periscope(angle=5)
        if "e" in pressed_keys:  # Rotate mast right
            coral.rotate_periscope(angle=-5)

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
            coral.toggle_resource_list()
        elif key == Key.space:
            print("Toggling obstacle list display.")
            coral.toggle_obstacle_list()
        elif key == Key.esc:
            print("Exiting...")
            stop_loop = True
            return False  # Stop listener

        # Handle resource and obstacle placement
        if "o" in pressed_keys:
            print("Placing resource...")
            # Fetch ultrasound measurement for dynamic distance
            distance = coral.get_ultrasound_measurement()
            coral.map_resource(distance=distance, size=5)
        if "p" in pressed_keys:
            print("Placing obstacle...")
            # Fetch ultrasound measurement for dynamic distance
            distance = coral.get_ultrasound_measurement()
            coral.map_obstacle(distance=distance, size=15)

        if key.char == "t":
            global scanning_enabled
            scanning_enabled = not scanning_enabled
            coral.toggle_scan()

        if key.char == "m":
            coral.save_map("latest.json")

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