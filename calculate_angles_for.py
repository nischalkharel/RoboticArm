import math


BASE_OFFSET = 90

# Lengths of each section of the robotic arm (in inches)
L1 = 4.0  # Length from shoulder to elbow
L2 = 4.2  # Length from elbow to wrist
L3 = 5.25  # Length from wrist to gripper
GRIPPER_LENGTH = 6.5  # Length of the gripper fingers

# Angle limits for each servo
BASE_MIN = 0
BASE_MAX = 180
SHOULDER_MIN = 90
SHOULDER_MAX = 270
ELBOW_MIN = 65
ELBOW_MAX = 180
WRIST_MIN = 0
WRIST_MAX = 90

y_diff_neg = True #because initially G_y would be 7 more than 4 so true

def calculate(x, y, z):
    theta_base = math.atan2(abs(x), abs(z))  # Base angle in radians, taking into account the sign of x
    theta_base_deg = math.degrees(theta_base)  # Proper indentation here

    # Adjust theta_base_deg based on the reference point of the base motor (90 degrees is straight ahead)
    if x >= 0:
        theta_base_deg = BASE_OFFSET - theta_base_deg  # Right side, decrease from 90
    else:
        theta_base_deg = BASE_OFFSET + theta_base_deg  # Left side, increase from 90
        
    theta_base_deg = max(BASE_MIN, min(BASE_MAX, theta_base_deg))

    G_z = 0  # Start with G_z being 0 (horizontal side)
    G_y = GRIPPER_LENGTH  # Initially, G_y is equal to the gripper length (vertical side)

    while G_z <= z:
        # Step 1: Calculate the remaining vertical distance from shoulder to target (4 - G_y)
        shoulder_to_target_y = L1 - G_y
			
        # Step 2: Calculate the horizontal distance from shoulder to target (Z - G_z)
        shoulder_to_target_distance_after_base_rotated = math.sqrt(abs(x)**2 + z**2)
        shoulder_to_target_z = shoulder_to_target_distance_after_base_rotated - G_z


        # Step 3: Check if the target is reachable
        if shoulder_to_target_z <= (L2 + L3):
                # Step 4: Calculate the hypotenuse (distance from shoulder to target)
            # when G_y is more than 4inches
            if shoulder_to_target_y < 0:
                #if G_y is more than 4.0 that means shoulder will be aiming target above its joint so we need to get the triangle little differently
                y_diff_neg = True
                hypotenuse = math.sqrt(abs(shoulder_to_target_y)**2 + shoulder_to_target_z**2)
            else:
                y_diff_neg = False
                hypotenuse = math.sqrt(shoulder_to_target_y**2 + shoulder_to_target_z**2)

        

            # Step 5: Use the law of cosines to find the angles
            try:
                cos_theta_elbow = (L2**2 + L3**2 - hypotenuse**2) / (2 * L2 * L3)
                cos_theta_elbow = max(-1, min(1, cos_theta_elbow))  # Clamp value to be within [-1, 1]
                theta_elbow = math.acos(cos_theta_elbow)  # Elbow angle in radians
                theta_elbow_deg = math.degrees(theta_elbow)

                cos_theta_shoulder = (L2**2 + hypotenuse**2 - L3**2) / (2 * L2 * hypotenuse)
                cos_theta_shoulder = max(-1, min(1, cos_theta_shoulder))  # Clamp value to be within [-1, 1]
                theta_shoulder = math.acos(cos_theta_shoulder)  # Shoulder angle in radians

                if y_diff_neg:
                    incline_angle = math.degrees(math.atan2(abs(shoulder_to_target_y), shoulder_to_target_z))  # atan(y/z)
                    theta_shoulder_deg = math.degrees(theta_shoulder) + incline_angle + 90 # Adjust shoulder angle from the verticle line
                else:
                    incline_angle = math.degrees(math.atan2(shoulder_to_target_z, shoulder_to_target_y))  # atan(z/y)
                    theta_shoulder_deg = math.degrees(theta_shoulder) + incline_angle 

                # Step 6: Calculate wrist angle based on G_y and L_4 using normal triangle solving
                if G_z == 0:
                    wrist_angle = 0
                else:
                    wrist_angle = math.atan2(G_z, G_y)  # Wrist angle in radians between G_y and L_4
                
                theta_wrist_deg = math.degrees(wrist_angle)
                theta_wrist_deg = max(WRIST_MIN, min(WRIST_MAX, theta_wrist_deg))

                # Step 7: Check if the calculated angles are within the valid range
                if SHOULDER_MIN <= theta_shoulder_deg <= SHOULDER_MAX and ELBOW_MIN <= theta_elbow_deg <= ELBOW_MAX:
                    # Print calculated angles for debugging
                    realShoulderAngle = theta_shoulder_deg - 85
                    realElbowAngle = 245 - theta_elbow_deg
                    print("Valid angles found.")
                    return  theta_base_deg, realShoulderAngle, realElbowAngle, theta_wrist_deg
            except ValueError:
                pass  # Ignore math domain errors and continue adjusting G_z

        else:
            # Increase G_z by 1% of Z to adjust the gripper position and recalculate
            G_z += 0.01 * z

    print("Error: Could not find valid angles for the given target.")
