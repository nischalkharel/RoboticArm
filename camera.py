import cv2
import cv2.aruco as aruco
import numpy as np
from picamera2 import Picamera2

camera_matrix = np.loadtxt("/home/nischalkharel2002/Desktop/robotic_arm_code/camera_matrix.dat")
dist_coeffs = np.loadtxt("/home/nischalkharel2002/Desktop/robotic_arm_code/dist_coeffs.dat")


# Initialize Picamera2
picam2 = Picamera2()
# Set the resolution (lower resolution to reduce memory usage if needed)
config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
picam2.start()

# ArUco marker dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

# Function to continuously try to find the ArUco marker and return coordinates
def get_marker_coordinates():
    while True:
        # Capture frame from the camera
        frame = picam2.capture_array()

        # Ensure the frame is valid (not empty)
        if frame is None or frame.size == 0:
            continue

        # Convert frame to BGR format (Picamera2 outputs RGB by default)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Convert frame to grayscale for ArUco detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers in the frame
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        print("trying to detect the block")
        if ids is not None:
            # Estimate the pose of the marker
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.0235, camera_matrix, dist_coeffs)  # Marker size in meters (3.2 cm)
            for i in range(len(ids)):
                # Get translation vector (tvec) for distance calculation and convert to inches
                x_m, y_m, z_m = tvecs[i][0]  # (x, y, z) in meters
                x_in, y_in, z_in = x_m * 39.3701, y_m * 39.3701, z_m * 39.3701  # Convert to inches
                x_in += 1.87
                y_in -= 1
                return x_in, y_in, z_in

# Function to be used externally to get the coordinates
if __name__ == "__main__":
    try:
        x, y, z = get_marker_coordinates()
        
        print(f"X: {x:.2f} in, Y: {y:.2f} in, Z: {z:.2f} in")
    finally:
        # Release resources
        picam2.stop()
