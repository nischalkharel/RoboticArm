import cv2
import numpy as np
import os
import time
from picamera2 import Picamera2

# Checkerboard dimensions (internal corners)
CHECKERBOARD = (5, 7)  # (columns-1, rows-1)

# Real-world size of each square on the checkerboard in millimeters
SQUARE_SIZE = 20  # mm

# Termination criteria for corner subpixel accuracy (max iterations or accuracy threshold)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Arrays to store object points and image points from all the images
objpoints = []  # 3D points in the real world
imgpoints = []  # 2D points in the image plane

# Prepare object points based on the real checkerboard layout
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE  # Scale by the square size to get real-world coordinates

# Directory to save calibration images
calibration_dir = "calibration_images"
os.makedirs(calibration_dir, exist_ok=True)

# Initialize Picamera2
picam2 = Picamera2()
# Set the resolution (lower resolution to reduce memory usage if needed)
config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
picam2.start()

# Countdown before starting to take pictures with live camera view
print("Starting countdown before taking pictures...")
for i in range(30, 0, -1):
    frame = picam2.capture_array()
    cv2.putText(frame, f"Starting in {i} seconds...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Live View', frame)
    cv2.waitKey(1000)

# Capture 20 calibration images with 10-second intervals
for i in range(20):
    for j in range(10, 0, -1):
        frame = picam2.capture_array()
        cv2.putText(frame, f"Capturing image {i + 1} in {j} seconds...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Live View', frame)
        cv2.waitKey(1000)

    print(f"Capturing image {i + 1}...")
    frame = picam2.capture_array()
    image_path = os.path.join(calibration_dir, f"calibration_image_{i + 1}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"Image {i + 1} saved to {image_path}")

print("Finished capturing calibration images.")

# Load images of the checkerboard taken from different angles
images = [os.path.join(calibration_dir, f) for f in os.listdir(calibration_dir) if f.endswith(".jpg")]

gray = None
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the checkerboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    # If found, add object points and refined corner locations
    if ret:
        objpoints.append(objp)

        # Refine corner locations for greater accuracy
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('Checkerboard', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Calibration step
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save the calibration results to use in other programs
np.savetxt("camera_matrix.dat", camera_matrix)
np.savetxt("dist_coeffs.dat", dist_coeffs)

# Print calibration results
print("Camera matrix:")
print(camera_matrix)
print("\nDistortion coefficients:")
print(dist_coeffs)

# Test undistortion on one image
img = cv2.imread(images[0])
h, w = img.shape[:2]
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

# Undistort the image
dst = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# Crop the image if there is any black border
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

# Display original and undistorted images
cv2.imshow("Original Image", img)
cv2.imshow("Undistorted Image", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Release Picamera2 resources
picam2.stop()
