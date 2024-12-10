from time import sleep
from adafruit_servokit import ServoKit

# Initialize the ServoKit instance for 16 channels (controls up to 16 servos)
kit = ServoKit(channels=16)

# Dictionary to store the current angles of each motor
current_angles = {
    0: 90,  # Base motor starting at 90 degrees (facing straight ahead)
    1: 90,  # Shoulder motor starting at 90 degrees (neutral position)
    2: 90,  # Elbow motor starting at 90 degrees (neutral position)
    3: 45,  # Wrist motor starting at 45 degrees (neutral position)
    4: 90   # Gripper motor starting fully open at 90 degrees
}

# Function to drive a motor to the specified angle smoothly
def move_motor(motor_id, target_angle):
    if motor_id not in current_angles:
        print(f"Error: Invalid motor ID {motor_id}. Motor ID must be between 0 and 4.")
        return

    if target_angle < 0 or target_angle > 180:
        print(f"Error: Target angle {target_angle} out of range. Must be between 0 and 180 degrees.")
        return

    current_angle = current_angles[motor_id]
    step = 1 if target_angle > current_angle else -1

    # Slowly move to the target angle
    for angle in range(int(current_angle), int(target_angle), step):
        kit.servo[motor_id].angle = angle
        current_angles[motor_id] = angle
        sleep(0.02)  # Adjust the sleep time to control the speed of movement

    # Set the final target angle
    kit.servo[motor_id].angle = int(target_angle)
    current_angles[motor_id] = target_angle
    print(f"Motor {motor_id} moved to {target_angle} degrees.")

def reset_motors():
	move_motor(4,90)
	sleep(.5)
	move_motor(1,90)
	sleep(0.1)
	move_motor(2,90)
	sleep(0.1)
	move_motor(3,45)
	sleep(0.1)
	move_motor(0,90)
	sleep(3)
	
	
def pick_up():
	move_motor(4,150)
	sleep(.5)
	move_motor(1,90)
	sleep(0.1)
	move_motor(0, 90)
	sleep(0.1)
	move_motor(2,90)
	sleep(0.1)
	move_motor(3,45)
	sleep(3)

def place_it():
	move_motor(0,174)
	sleep(.5)
	move_motor(1,108)
	sleep(0.3)
	move_motor(2, 155)
	sleep(0.3)
	move_motor(3,11)
	sleep(0.1)
	move_motor(4, 100)
	sleep(3)
