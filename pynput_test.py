from pynput.keyboard import Listener, Key  # Import Key explicitly

def on_press(key):
    print(f"Key pressed: {key}")

def on_release(key):
    print(f"Key released: {key}")
    if key == Key.esc:  # Now this will work
        return False  # Stop listener

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()