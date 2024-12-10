import calculate_angles_for
import move_motor
import camera
from time import sleep
from audio_in import listen_to_microphone
from audio_out import speak_text

def get_motor_angles(x, y, z):
    return calculate_angles_for.calculate(x, y, z)

def main():
    x_target, y_target, z_target = camera.get_marker_coordinates()
    x_target = x_target - 1.5
    z_target = z_target + 0.17 * z_target
    angles = get_motor_angles(x_target, y_target, z_target)
    print(f"x-Target: {x_target:.2f}°")
    print(f"y-Target: {y_target:.2f}°")
    print(f"z-Target: {z_target:.2f}°")
    if angles:
        base_angle, shoulder_angle, elbow_angle, wrist_angle = angles
        print(f"Base Angle: {base_angle:.2f}°")
        print(f"Shoulder Angle: {shoulder_angle:.2f}°")
        print(f"Elbow Angle: {elbow_angle:.2f}°")
        print(f"Wrist Angle: {wrist_angle:.2f}°")
        move_motor.reset_motors()
        move_motor.move_motor(0, base_angle)
        move_motor.move_motor(2, elbow_angle)
        move_motor.move_motor(3, wrist_angle)
        move_motor.move_motor(1, shoulder_angle)
        move_motor.move_motor(4, 148)
        sleep(1)
        move_motor.pick_up()
        move_motor.place_it()
        move_motor.reset_motors()
    else:
        print("Error: Could not find valid angles for the given target.")

if __name__ == "__main__":
    while True:
        recognized_text = listen_to_microphone()
        if recognized_text == "activate now":
            speak_text("Please, wait,    The arm, is, activating!")
            main()
            speak_text("I  am, ready, to, go, again!")
