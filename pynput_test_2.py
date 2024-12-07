from pynput.keyboard import Listener, Key
import time
import threading

# Track pressed keys
pressed_keys = set()
stop_loop = False  # Flag to stop the continuous processing loop
lock = threading.Lock()  # Lock for thread-safe access to pressed_keys

def on_press(key):
    global stop_loop
    try:
        with lock:
            # Handle alphanumeric keys
            if hasattr(key, 'char') and key.char:
                pressed_keys.add(key.char.lower())  # Add lowercase char to set
            # Handle special keys
            elif key == Key.esc:
                print("ESC pressed. Exiting...")
                stop_loop = True
                return False  # Stop the listener
    except Exception as e:
        print(f"Error in on_press: {e}")

def on_release(key):
    try:
        with lock:
            # Handle alphanumeric keys
            if hasattr(key, 'char') and key.char:
                pressed_keys.discard(key.char.lower())  # Remove key from set
            # Handle special keys
            elif key == Key.esc:
                pressed_keys.discard("esc")
    except Exception as e:
        print(f"Error in on_release: {e}")

def process_keys():
    """Continuously process key states to handle simultaneous and individual actions."""
    global stop_loop
    while not stop_loop:
        with lock:
            if pressed_keys:
                # Handle specific key combinations
                if "w" in pressed_keys and "d" in pressed_keys:  # Forward + Turn Right
                    print("Moving forward and turning right")
                elif "w" in pressed_keys and "a" in pressed_keys:  # Forward + Turn Left
                    print("Moving forward and turning left")
                elif "s" in pressed_keys and "d" in pressed_keys:  # Reverse + Turn Right
                    print("Reversing and turning right")
                elif "s" in pressed_keys and "a" in pressed_keys:  # Reverse + Turn Left
                    print("Reversing and turning left")
                else:
                    # Handle individual keys
                    for key in pressed_keys:
                        if key == "w":
                            print("Moving forward")
                        elif key == "s":
                            print("Reversing")
                        elif key == "a":
                            print("Turning left")
                        elif key == "d":
                            print("Turning right")
        time.sleep(0.1)  # Process every 100ms to prevent high CPU usage

def start_listener():
    """Start the key listener."""
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Start the key listener in a separate thread
listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()

# Start the continuous key processing loop
try:
    process_keys()
except KeyboardInterrupt:
    stop_loop = True
    listener_thread.join()
    print("Exiting...")