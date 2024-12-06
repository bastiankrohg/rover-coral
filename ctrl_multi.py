import platform
from coral_multi import Coral

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
    print("Ø: Rotate periscope left | Æ: Rotate periscope right")

    # State tracking for continuous movement
    move_forward = False
    move_backward = False
    turn_left = False
    turn_right = False

    def on_press(key):
        nonlocal move_forward, move_backward, turn_left, turn_right
        try:
            if key.char == "w":
                move_forward = True
                coral.drive_forward(speed=5)
            elif key.char == "s":
                move_backward = True
                coral.reverse(speed=5)
            elif key.char == "a":
                turn_left = True
                if move_forward:
                    coral.turn_left(angle=15)  # Moving + turning
                elif move_backward:
                    coral.turn_left(angle=-15)  # Reversing + turning
                else:
                    coral.rotate_on_spot(angle=-15)  # Stationary rotation
            elif key.char == "d":
                turn_right = True
                if move_forward:
                    coral.turn_right(angle=15)  # Moving + turning
                elif move_backward:
                    coral.turn_right(angle=-15)  # Reversing + turning
                else:
                    coral.rotate_on_spot(angle=15)  # Stationary rotation
            elif key.char == " ":
                coral.stop_movement()
        except AttributeError:
            if key == keyboard.Key.esc:
                print("[DEBUG] Exiting manual control.")
                return False

    def on_release(key):
        nonlocal move_forward, move_backward, turn_left, turn_right
        try:
            if key.char == "w":
                move_forward = False
                coral.stop_movement()
            elif key.char == "s":
                move_backward = False
                coral.stop_movement()
            elif key.char == "a":
                turn_left = False
                coral.stop_movement()
            elif key.char == "d":
                turn_right = False
                coral.stop_movement()
        except AttributeError:
            pass

    print("[DEBUG] Starting manual control...")
    if platform.system() == "Darwin":
        from pynput.keyboard import Listener
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    else:
        # Use keyboard library for other platforms
        try:
            while True:
                if keyboard.is_pressed("w"):
                    move_forward = True
                    coral.drive_forward(speed=5)
                elif keyboard.is_pressed("s"):
                    move_backward = True
                    coral.reverse(speed=5)
                elif keyboard.is_pressed("a"):
                    turn_left = True
                    coral.turn_left(angle=15)
                elif keyboard.is_pressed("d"):
                    turn_right = True
                    coral.turn_right(angle=15)
                elif keyboard.is_pressed("q"):
                    coral.rotate_on_spot(angle=-15)
                elif keyboard.is_pressed("e"):
                    coral.rotate_on_spot(angle=15)
                elif keyboard.is_pressed("o"):
                    distance = coral.get_ultrasound_measurement() or 10
                    coral.place_resource(distance=distance)
                elif keyboard.is_pressed("p"):
                    distance = coral.get_ultrasound_measurement() or 10
                    coral.place_obstacle(distance=distance)
                elif keyboard.is_pressed(" "):
                    coral.stop_movement()
                elif keyboard.is_pressed("esc"):
                    print("[DEBUG] Exiting manual control.")
                    break
        except KeyboardInterrupt:
            print("[DEBUG] Manual control interrupted.")


if __name__ == "__main__":
    manual_control()