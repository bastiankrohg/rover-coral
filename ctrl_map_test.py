import platform
from coral_map_test import Coral

if platform.system() == "Darwin":  # Darwin is the system name for macOS
    from pynput import keyboard  # Use pynput for macOS
else:
    import keyboard  # Use keyboard for other platforms


def manual_control():
    coral = Coral()
    print("Manual control started. Use the keys below:")
    print("W: Drive forward | S: Reverse")
    print("A: Turn left | D: Turn right")
    print("Q: Rotate left on spot | E: Rotate right on spot")
    print("H: Toggle headlights | L: Toggle wheel LEDs")
    print("O: Place resource | P: Place obstacle")
    print("Space: Stop movement | ESC: Exit")

    def on_press(key):
        try:
            if key.char == "w":
                coral.drive_forward(speed=5)  # Smooth, continuous updates
            elif key.char == "s":
                coral.reverse(speed=5)
            elif key.char == "a":
                coral.turn_left(angle=15)
            elif key.char == "d":
                coral.turn_right(angle=15)
            elif key.char == "q":
                print("[DEBUG] Rotate left on spot key pressed.")
                coral.rotate_on_spot(angle=-15)
            elif key.char == "e":
                print("[DEBUG] Rotate right on spot key pressed.")
                coral.rotate_on_spot(angle=15)
            elif key.char == "o":
                print("[DEBUG] Place resource key pressed.")
                distance = coral.get_ultrasound_measurement() or 0
                coral.place_resource(distance=distance)
            elif key.char == "p":
                print("[DEBUG] Place obstacle key pressed.")
                distance = coral.get_ultrasound_measurement() or 0
                coral.place_obstacle(distance=distance)
            elif key.char == " ":
                coral.stop_movement()
            elif key.char == "ø":
                print("[DEBUG] Rotate periscope left key pressed.")
                coral.rotate_periscope(10)
            elif key.char == "æ":
                print("[DEBUG] Rotate periscope right key pressed.")
                coral.rotate_periscope(-10)
            elif key.char == "h":
                coral.control_headlights(on=True)
            elif key.char == "l":
                for wheel in range(6):  # Example toggle for all wheels
                    coral.control_wheel_leds(wheel, on=True)
        except AttributeError:
            if key == keyboard.Key.esc:
                print("[DEBUG] Exiting manual control.")
                return False

    print("[DEBUG] Starting manual control...")
    if platform.system() == "Darwin":
        from pynput.keyboard import Listener
        with Listener(on_press=on_press) as listener:
            listener.join()
    else:
        # Use keyboard library for other platforms
        try:
            while True:
                if keyboard.is_pressed("w"):
                    coral.drive_forward(speed=5)
                elif keyboard.is_pressed("s"):
                    coral.reverse(speed=5)
                elif keyboard.is_pressed("a"):
                    coral.turn_left(angle=15)
                elif keyboard.is_pressed("d"):
                    coral.turn_right(angle=15)
                elif keyboard.is_pressed("q"):
                    coral.rotate_on_spot(angle=-15)
                elif keyboard.is_pressed("e"):
                    coral.rotate_on_spot(angle=15)
                elif keyboard.is_pressed("o"):
                    coral.place_resource(distance=10)
                elif keyboard.is_pressed("p"):
                    coral.place_obstacle(distance=10)
                elif keyboard.is_pressed(" "):
                    coral.stop_movement()
                elif keyboard.is_pressed("esc"):
                    print("[DEBUG] Exiting manual control.")
                    break
        except KeyboardInterrupt:
            print("[DEBUG] Manual control interrupted.")


if __name__ == "__main__":
    manual_control()