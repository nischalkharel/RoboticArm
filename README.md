# RoboticArm
arm.py: This is the main file that ties everything together. It listens for voice commands and coordinates the overall process, from detecting the block to moving the arm.


camera.py: This handles detecting the ArUco marker, calculating the block's position in x, y, z, and returning those coordinates.


calculate_angles_for.py: Using the block’s coordinates, this file calculates the angles for each joint of the arm. I simplified inverse kinematics into something more intuitive for me, which worked better than traditional IK.


move_motor.py: This file sends the calculated angles to the servos, making the arm move smoothly.


audio_in.py and audio_out.py: These files handle the voice interaction. One listens for commands through the microphone, and the other sends audio feedback through the speaker.
