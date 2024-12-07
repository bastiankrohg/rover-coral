import platform

if platform.system() == "Darwin":  # macOS specific
    from pynput import keyboard  # Use pynput for macOS
else:
    import keyboard  # Use keyboard for other platforms

from coral_control import Coral

def manual_control():
    coral = Coral()
    print("Manual control started. Use the keys below:")
    print("W: Drive forward | S: Reverse")
    print("A: Turn left | D: Turn right")
    print("Q: Rotate left on spot | E: Rotate right on spot")
    print("H: Toggle headlights | L: Toggle wheel LEDs")
    print("P: Rotate periscope | Space: Stop movement | ESC: Exit")

    pressed_keys = set()
    headlights_on = False
    wheel_leds_on = [False] * 6  # Keep track of LEDs for 6 wheels

    def handle_combined_keys():
        """Handle simultaneous key presses for smooth combined actions."""
        if "w" in pressed_keys:
            coral.drive_forward(speed=50)
        if "s" in pressed_keys:
            coral.reverse(speed=50)
        if "a" in pressed_keys and "w" in pressed_keys:
            coral.turn_left(angle=5)
        elif "a" in pressed_keys and "s" in pressed_keys:
            coral.turn_left(angle=-5)
        elif "a" in pressed_keys:
            coral.rotate_on_spot(angle=-15)
        if "d" in pressed_keys and "w" in pressed_keys:
            coral.turn_right(angle=5)
        elif "d" in pressed_keys and "s" in pressed_keys:
            coral.turn_right(angle=-5)
        elif "d" in pressed_keys:
            coral.rotate_on_spot(angle=15)

    def on_press(key):
        try:
            if key.char not in pressed_keys:
                pressed_keys.add(key.char)
                if key.char in {"w", "s", "a", "d"}:
                    handle_combined_keys()
                elif key.char == "q":
                    print("[DEBUG] Rotate left on spot key pressed.")
                    coral.rotate_on_spot(angle=-15)
                elif key.char == "e":
                    print("[DEBUG] Rotate right on spot key pressed.")
                    coral.rotate_on_spot(angle=15)
                elif key.char == "h":
                    nonlocal headlights_on
                    headlights_on = not headlights_on
                    coral.control_headlights(headlights_on)
                elif key.char == "l":
                    for wheel in range(6):
                        wheel_leds_on[wheel] = not wheel_leds_on[wheel]
                        coral.control_wheel_leds(wheel, wheel_leds_on[wheel])
                elif key.char == "p":
                    angle = float(input("Enter periscope angle: "))
                    coral.rotate_periscope(angle)
                elif key.char == " ":
                    print("[DEBUG] Stop movement key pressed.")
                    coral.stop_movement()
        except AttributeError:
            if key == keyboard.Key.esc:
                print("[DEBUG] Exiting manual control.")
                return False

    def on_release(key):
        try:
            if key.char in pressed_keys:
                pressed_keys.remove(key.char)
                if not pressed_keys:  # Stop all movement if no keys are pressed
                    coral.stop_movement()
        except AttributeError:
            pass

    print("[DEBUG] Starting manual control...")
    if platform.system() == "Darwin":
        from pynput.keyboard import Listener
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    else:
        # Use keyboard library for non-macOS systems
        try:
            while True:
                for key in "wasdqel ":
                    if keyboard.is_pressed(key):
                        if key not in pressed_keys:
                            pressed_keys.add(key)
                            on_press(key)
                    else:
                        if key in pressed_keys:
                            pressed_keys.remove(key)
                            on_release(key)
                if keyboard.is_pressed("esc"):
                    print("[DEBUG] Exiting manual control.")
                    break
        except KeyboardInterrupt:
            print("[DEBUG] Manual control interrupted.")

if __name__ == "__main__":
    print("[DEBUG] Starting manual control application...")
    manual_control()