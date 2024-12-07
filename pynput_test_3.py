from pynput.keyboard import Listener, Key
import time
import threading

# Track pressed keys
pressed_keys = set()
stop_loop = False  # Flag to stop the continuous processing loop

# Flags for resource/obstacle placement
placing_resource = False
placing_obstacle = False

def on_press(key):
    """Handle key press events."""
    global placing_resource, placing_obstacle, stop_loop

    try:
        # Handle alphanumeric keys
        if hasattr(key, 'char') and key.char:
            pressed_keys.add(key.char.lower())

        # Handle special keys
        elif key in (Key.tab, Key.space, Key.up, Key.down, Key.left, Key.right, Key.enter, Key.esc):
            pressed_keys.add(key)

            if key == Key.tab:
                print("Toggling resource list display.")
            elif key == Key.space:
                print("Toggling obstacle list display.")
            elif key == Key.esc:
                print("Exiting...")
                stop_loop = True
                return False  # Stop listener
    except Exception as e:
        print(f"Error in on_press: {e}")

def on_release(key):
    """Handle key release events."""
    global placing_resource, placing_obstacle

    try:
        # Remove alphanumeric keys from the set
        if hasattr(key, 'char') and key.char:
            pressed_keys.discard(key.char.lower())

        # Handle special keys
        elif key in (Key.tab, Key.space, Key.up, Key.down, Key.left, Key.right, Key.enter, Key.esc):
            pressed_keys.discard(key)

        if hasattr(key, 'char') and key.char == "o":
            placing_resource = False
            print("Stopped placing resource.")
        elif hasattr(key, 'char') and key.char == "p":
            placing_obstacle = False
            print("Stopped placing obstacle.")
    except Exception as e:
        print(f"Error in on_release: {e}")

def process_keys():
    """Continuously process key states for combined and individual actions."""
    global stop_loop

    while not stop_loop:
        if pressed_keys:
            # Handle directional movement
            if Key.up in pressed_keys:
                print("Moving rover forward.")
            if Key.down in pressed_keys:
                print("Moving rover backward.")
            if Key.left in pressed_keys and Key.up in pressed_keys:
                print("Rotating rover and mast left while moving forward.")
            elif Key.left in pressed_keys and Key.down in pressed_keys:
                print("Rotating rover and mast left while moving backward.")
            elif Key.left in pressed_keys:
                print("Rotating rover and mast left.")
            if Key.right in pressed_keys and Key.up in pressed_keys:
                print("Rotating rover and mast right while moving forward.")
            elif Key.right in pressed_keys and Key.down in pressed_keys:
                print("Rotating rover and mast right while moving backward.")
            elif Key.right in pressed_keys:
                print("Rotating rover and mast right.")
            if "a" in pressed_keys:
                print("Rotating mast left.")
            if "d" in pressed_keys:
                print("Rotating mast right.")
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