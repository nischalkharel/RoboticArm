import math
import curses
from adafruit_servokit import ServoKit

# Initialize the ServoKit instance for 16 channels (controls up to 16 servos)
kit = ServoKit(channels=16)

# Lengths of each section of the robotic arm (in centimeters, update these values according to your arm)
L1 = 12.7  # Length from shoulder to elbow
L2 = 13.97  # Length from elbow to wrist

# Initial angles for each servo
base_angle = 90 # Starting at straight ahead
shoulder_angle = 95  # Mid-range starting point
elbow_angle = 80  # Mid-range starting point
wrist_angle = 45  # Neutral starting position
gripper_angle = 90  # Starting fully open

# Angle limits for each servo
BASE_MIN = 0
BASE_MAX = 180
SHOULDER_MAX = 15
ELBOW_MIN = 60
ELBOW_MAX = 180
WRIST_MIN = 0
WRIST_MAX = 90
GRIPPER_MIN = 90
GRIPPER_MAX = 148

# Angle step size for smoother movements
ANGLE_STEP = 0.5

# Function to display the current angles
def display_angles(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Base Angle: {base_angle:.2f}°")
    stdscr.addstr(1, 0, f"Shoulder Angle: {shoulder_angle:.2f}°")
    stdscr.addstr(2, 0, f"Elbow Angle: {elbow_angle:.2f}°")
    stdscr.addstr(3, 0, f"Wrist Angle: {wrist_angle:.2f}°")
    stdscr.addstr(4, 0, f"Gripper Angle: {gripper_angle:.2f}°")
    stdscr.refresh()

# Function to update the servos
def update_servos():
    kit.servo[0].angle = base_angle       # Base servo (controls left-right rotation)
    kit.servo[1].angle = shoulder_angle   # Shoulder servo (controls up-down movement from the base)
    kit.servo[2].angle = elbow_angle      # Elbow servo (controls bending of the arm)
    kit.servo[3].angle = wrist_angle      # Wrist servo (controls wrist orientation)
    kit.servo[4].angle = gripper_angle    # Gripper servo (controls opening and closing)

# Function to adjust limits based on current angles to prevent collisions or hitting the ground
def adjust_limits():
    global SHOULDER_MAX, ELBOW_MIN
    # Adjust shoulder maximum limit based on the elbow angle to avoid hitting the ground
    if elbow_angle > 100:
        SHOULDER_MAX = 150  # If elbow is high, shoulder can move more freely
    else:
        SHOULDER_MAX = 120  # If elbow is low, restrict shoulder to avoid collision

    # Adjust elbow minimum limit based on the shoulder angle
    if shoulder_angle < 60:
        ELBOW_MIN = 60  # Restrict elbow movement when shoulder is too low
    else:
        ELBOW_MIN = 60  # Restore normal elbow limit

# Main loop to control the servos with keyboard using curses
def main(stdscr):
    global base_angle, shoulder_angle, elbow_angle, wrist_angle, gripper_angle

    # Hide the cursor
    curses.curs_set(0)

    # Instructions
    stdscr.addstr(6, 0, "Use 'w' and 's' to control the shoulder, 'a' and 'd' for the wrist, arrow keys for the base and elbow, 'o' to open and 'c' to close gripper. Press 'q' to exit.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()

        # Adjust limits based on current angles
        adjust_limits()

        # Shoulder control
        if key == ord('w'):
            if shoulder_angle < SHOULDER_MAX:
                shoulder_angle += ANGLE_STEP
            else:
                stdscr.addstr(8, 0, f"Shoulder limit hit at {shoulder_angle:.2f}°")
        elif key == ord('s'):
            shoulder_angle -= ANGLE_STEP
        else:
            stdscr.addstr(8, 0, " " * 50)

        # Wrist control
        if key == ord('a'):
            if wrist_angle > WRIST_MIN:
                wrist_angle -= ANGLE_STEP
            else:
                stdscr.addstr(9, 0, f"Wrist limit hit at {wrist_angle:.2f}°")
        elif key == ord('d'):
            if wrist_angle < WRIST_MAX:
                wrist_angle += ANGLE_STEP
            else:
                stdscr.addstr(9, 0, f"Wrist limit hit at {wrist_angle:.2f}°")
        else:
            stdscr.addstr(9, 0, " " * 50)

        # Base control
        if key == curses.KEY_LEFT:
            if base_angle > BASE_MIN:
                base_angle -= ANGLE_STEP
            else:
                stdscr.addstr(10, 0, f"Base limit hit at {base_angle:.2f}°")
        elif key == curses.KEY_RIGHT:
            if base_angle < BASE_MAX:
                base_angle += ANGLE_STEP
            else:
                stdscr.addstr(10, 0, f"Base limit hit at {base_angle:.2f}°")
        else:
            stdscr.addstr(10, 0, " " * 50)

        # Elbow control
        if key == curses.KEY_UP:
            if elbow_angle < ELBOW_MAX:
                elbow_angle += ANGLE_STEP
            else:
                stdscr.addstr(11, 0, f"Elbow limit hit at {elbow_angle:.2f}°")
        elif key == curses.KEY_DOWN:
            if elbow_angle > ELBOW_MIN:
                elbow_angle -= ANGLE_STEP
            else:
                stdscr.addstr(11, 0, f"Elbow limit hit at {elbow_angle:.2f}°")
        else:
            stdscr.addstr(11, 0, " " * 50)

        # Gripper control
        if key == ord('o'):
            if gripper_angle > GRIPPER_MIN:
                gripper_angle = GRIPPER_MIN  # Fully open the gripper
            stdscr.addstr(12, 0, f"Gripper opened to {gripper_angle:.2f}°")
        elif key == ord('c'):
            if gripper_angle < GRIPPER_MAX:
                gripper_angle = GRIPPER_MAX  # Fully close the gripper
            stdscr.addstr(12, 0, f"Gripper closed to {gripper_angle:.2f}°")
        else:
            stdscr.addstr(12, 0, " " * 50)

        # Update the servos with the new angles
        update_servos()
        display_angles(stdscr)

        # Exit the loop on 'q'
        if key == ord('q'):
            break

# Run the curses application
curses.wrapper(main)
