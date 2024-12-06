import platform

if platform.system() == "Darwin":  # Darwin is the system name for macOS
    from pynput import keyboard  # Use pynput for macOS
else:
    import keyboard  # Use keyboard for other platforms

from coral_v2 import Coral

def manual_control():
    coral = Coral()
    print("Manual control started. Use the keys below:")
    print("W: Drive forward | S: Reverse")
    print("A: Turn left | D: Turn right")
    print("Q: Rotate left on spot | E: Rotate right on spot")
    print("H: Toggle headlights | L: Toggle wheel LEDs")
    print("P: Rotate periscope | Space: Stop movement | ESC: Exit")

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
                elif key.char == "h":
                    print("[DEBUG] Toggle headlights key pressed.")
                    coral.control_headlights(True)  # Adjust to toggle if needed
                elif key.char == "l":
                    print("[DEBUG] Toggle wheel LEDs key pressed.")
                    coral.control_wheel_leds(0, True)  # Adjust to toggle if needed
                elif key.char == "p":
                    print("[DEBUG] Rotate periscope key pressed.")
                    angle = float(input("Enter periscope angle: "))
                    coral.rotate_periscope(angle)
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
            headlights_on = False
            wheel_leds_on = False
            print("[DEBUG] Starting keyboard library loop...")
            while True:
                if keyboard.is_pressed("w"):
                    print("[DEBUG] Drive forward key pressed.")
                    coral.drive_forward(speed=50)
                elif keyboard.is_pressed("s"):
                    print("[DEBUG] Reverse key pressed.")
                    coral.reverse(speed=50)
                elif keyboard.is_pressed("a"):
                    print("[DEBUG] Turn left key pressed.")
                    coral.turn_left(angle=30)
                elif keyboard.is_pressed("d"):
                    print("[DEBUG] Turn right key pressed.")
                    coral.turn_right(angle=30)
                elif keyboard.is_pressed("q"):
                    print("[DEBUG] Rotate left on spot key pressed.")
                    coral.rotate_on_spot(angle=-45)
                elif keyboard.is_pressed("e"):
                    print("[DEBUG] Rotate right on spot key pressed.")
                    coral.rotate_on_spot(angle=45)
                elif keyboard.is_pressed(" "):
                    print("[DEBUG] Stop movement key pressed.")
                    coral.stop_movement()
                elif keyboard.is_pressed("h"):
                    print("[DEBUG] Toggle headlights key pressed.")
                    headlights_on = not headlights_on
                    coral.control_headlights(headlights_on)
                elif keyboard.is_pressed("l"):
                    print("[DEBUG] Toggle wheel LEDs key pressed.")
                    wheel_leds_on = not wheel_leds_on
                    for wheel in range(6):
                        coral.control_wheel_leds(wheel, wheel_leds_on)
                elif keyboard.is_pressed("esc"):
                    print("[DEBUG] Exit key (ESC) pressed. Exiting manual control.")
                    break
        except KeyboardInterrupt:
            print("[DEBUG] Manual control interrupted.")

if __name__ == "__main__":
    print("[DEBUG] Starting manual control application...")
    manual_control()