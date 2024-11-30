import platform

if platform.system() == "Darwin":  # Darwin is the system name for macOS
    from pynput import keyboard  # Use pynput for macOS
else:
    import keyboard  # Use keyboard for other platforms

from coral import Coral

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
                    coral.drive_forward(speed=50)
                elif key.char == "s":
                    coral.reverse(speed=50)
                elif key.char == "a":
                    coral.turn_left(angle=30)
                elif key.char == "d":
                    coral.turn_right(angle=30)
                elif key.char == "q":
                    coral.rotate_on_spot(angle=-45)
                elif key.char == "e":
                    coral.rotate_on_spot(angle=45)
                elif key.char == " ":
                    coral.stop_movement()
                elif key.char == "h":
                    print("Toggling headlights")
                elif key.char == "l":
                    print("Toggling wheel LEDs")
                elif key.char == "p":
                    angle = float(input("Enter periscope angle: "))
                    coral.rotate_periscope(angle)
            except AttributeError:
                if key == keyboard.Key.esc:
                    print("Exiting manual control.")
                    return False

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    else:
        # Cross-platform implementation using the keyboard library
        try:
            headlights_on = False
            wheel_leds_on = False
            while True:
                if keyboard.is_pressed("w"):
                    coral.drive_forward(speed=50)
                elif keyboard.is_pressed("s"):
                    coral.reverse(speed=50)
                elif keyboard.is_pressed("a"):
                    coral.turn_left(angle=30)
                elif keyboard.is_pressed("d"):
                    coral.turn_right(angle=30)
                elif keyboard.is_pressed("q"):
                    coral.rotate_on_spot(angle=-45)
                elif keyboard.is_pressed("e"):
                    coral.rotate_on_spot(angle=45)
                elif keyboard.is_pressed(" "):
                    coral.stop_movement()
                elif keyboard.is_pressed("h"):
                    headlights_on = not headlights_on
                    coral.control_headlights(headlights_on)
                elif keyboard.is_pressed("l"):
                    wheel_leds_on = not wheel_leds_on
                    for wheel in range(6):
                        coral.control_wheel_leds(wheel, wheel_leds_on)
                elif keyboard.is_pressed("esc"):
                    print("Exiting manual control.")
                    break
        except KeyboardInterrupt:
            print("Manual control interrupted.")

if __name__ == "__main__":
    manual_control()