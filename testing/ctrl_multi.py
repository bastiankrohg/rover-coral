import platform
from testing.coral_multi import Coral

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

    # State tracking
    move_forward = False
    move_backward = False
    turn_left = False
    turn_right = False

    def handle_movement():
        """Handle combined key presses for movement and turning."""
        if move_forward and turn_left:
            coral.turn_left(angle=3)  # Forward + Left
        elif move_forward and turn_right:
            coral.turn_right(angle=3)  # Forward + Right
        elif move_backward and turn_left:
            coral.turn_left(angle=-3)  # Reverse + Left
        elif move_backward and turn_right:
            coral.turn_right(angle=-3)  # Reverse + Right
        elif move_forward:
            coral.drive_forward(speed=5)  # Forward
        elif move_backward:
            coral.reverse(speed=5)  # Reverse
        elif turn_left:
            coral.rotate_on_spot(angle=-5)  # Rotate Left
        elif turn_right:
            coral.rotate_on_spot(angle=5)  # Rotate Right
        else:
            coral.stop_movement()  # Stop

    def on_press(key):
        nonlocal move_forward, move_backward, turn_left, turn_right
        try:
            if key.char == "w":
                move_forward = True
            elif key.char == "s":
                move_backward = True
            elif key.char == "a":
                turn_left = True
            elif key.char == "d":
                turn_right = True
            elif key.char == "o":
                distance = coral.get_ultrasound_measurement() or 10
                coral.place_resource(distance=distance)
            elif key.char == "p":
                distance = coral.get_ultrasound_measurement() or 10
                coral.place_obstacle(distance=distance)
            elif key.char == " ":
                coral.stop_movement()
            handle_movement()
        except AttributeError:
            if key == keyboard.Key.esc:
                print("[DEBUG] Exiting manual control.")
                return False

    def on_release(key):
        nonlocal move_forward, move_backward, turn_left, turn_right
        try:
            if key.char == "w":
                move_forward = False
            elif key.char == "s":
                move_backward = False
            elif key.char == "a":
                turn_left = False
            elif key.char == "d":
                turn_right = False
            handle_movement()
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
                if keyboard.is_pressed("s"):
                    move_backward = True
                if keyboard.is_pressed("a"):
                    turn_left = True
                if keyboard.is_pressed("d"):
                    turn_right = True
                handle_movement()
                if keyboard.is_pressed("esc"):
                    print("[DEBUG] Exiting manual control.")
                    break
        except KeyboardInterrupt:
            print("[DEBUG] Manual control interrupted.")


if __name__ == "__main__":
    manual_control()