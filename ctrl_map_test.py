import platform
import time

if platform.system() == "Darwin":  # Darwin is the system name for macOS
    from pynput import keyboard  # Use pynput for macOS
else:
    import keyboard  # Use keyboard for other platforms

from coral_map_test import Coral


def manual_control():
    coral = Coral()
    print("Manual control started. Use the keys below:")
    print("W: Drive forward | S: Reverse")
    print("A: Turn left | D: Turn right")
    print("Q: Rotate left on spot | E: Rotate right on spot")
    print("O: Place resource | P: Place obstacle")
    print("Space: Stop movement | ESC: Exit")

    if platform.system() == "Darwin":
        # macOS-specific implementation using pynput
        def on_press(key):
            try:
                if key.char == "w":
                    print("[DEBUG] Drive forward key pressed.")
                    coral.drive_forward(speed=50)
                elif key.char == "s":
                    print("[DEBUG] Reverse key pressed.")
                    coral.reverse(speed=50)
                elif key.char == "a":
                    print("[DEBUG] Turn left key pressed.")
                    coral.turn_left(angle=30)
                elif key.char == "d":
                    print("[DEBUG] Turn right key pressed.")
                    coral.turn_right(angle=30)
                elif key.char == "q":
                    print("[DEBUG] Rotate left on spot key pressed.")
                    coral.rotate_on_spot(angle=-45)
                elif key.char == "e":
                    print("[DEBUG] Rotate right on spot key pressed.")
                    coral.rotate_on_spot(angle=45)
                elif key.char == "x":  # Replace space with x
                    print("[DEBUG] Stop movement key pressed.")
                    coral.stop_movement()
                elif key.char == "o":
                    print("[DEBUG] Place resource key pressed.")
                    distance = float(input("Enter distance to place resource: "))
                    coral.place_resource(distance)
                elif key.char == "p":
                    print("[DEBUG] Place obstacle key pressed.")
                    distance = float(input("Enter distance to place obstacle: "))
                    coral.place_obstacle(distance)
            except AttributeError:
                if key == keyboard.Key.esc:
                    print("[DEBUG] Exit key (ESC) pressed. Exiting manual control.")
                    return False

        print("[DEBUG] Starting pynput keyboard listener...")
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    else:
        # Cross-platform implementation using the keyboard library
        try:
            print("[DEBUG] Starting keyboard library loop...")
            while True:
                if keyboard.is_pressed("w"):
                    print("[DEBUG] Drive forward key pressed.")
                    coral.drive_forward(speed=50)
                    time.sleep(0.1)
                elif keyboard.is_pressed("s"):
                    print("[DEBUG] Reverse key pressed.")
                    coral.reverse(speed=50)
                    time.sleep(0.1)
                elif keyboard.is_pressed("a"):
                    print("[DEBUG] Turn left key pressed.")
                    coral.turn_left(angle=30)
                    time.sleep(0.1)
                elif keyboard.is_pressed("d"):
                    print("[DEBUG] Turn right key pressed.")
                    coral.turn_right(angle=30)
                    time.sleep(0.1)
                elif keyboard.is_pressed("q"):
                    print("[DEBUG] Rotate left on spot key pressed.")
                    coral.rotate_on_spot(angle=-45)
                    time.sleep(0.1)
                elif keyboard.is_pressed("e"):
                    print("[DEBUG] Rotate right on spot key pressed.")
                    coral.rotate_on_spot(angle=45)
                    time.sleep(0.1)
                elif keyboard.is_pressed(" "):
                    print("[DEBUG] Stop movement key pressed.")
                    coral.stop_movement()
                    time.sleep(0.1)
                elif keyboard.is_pressed("o"):
                    print("[DEBUG] Place resource key pressed.")
                    distance = float(input("Enter distance to place resource: "))
                    coral.place_resource(distance)
                    time.sleep(0.1)
                elif keyboard.is_pressed("p"):
                    print("[DEBUG] Place obstacle key pressed.")
                    distance = float(input("Enter distance to place obstacle: "))
                    coral.place_obstacle(distance)
                    time.sleep(0.1)
                elif keyboard.is_pressed("esc"):
                    print("[DEBUG] Exit key (ESC) pressed. Exiting manual control.")
                    break
        except KeyboardInterrupt:
            print("[DEBUG] Manual control interrupted.")

if __name__ == "__main__":
    print("[DEBUG] Starting manual control application...")
    manual_control()