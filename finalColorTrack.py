import cv2
import numpy as np
import L2_speed_control as sc
import L2_inverse_kinematics as ik
import L2_kinematics as kin
from time import sleep

# Constants
FORWARD_VELOCITY = 0.2  # Base forward velocity
ANGULAR_VELOCITY = 0.05  # Base angular velocity for adjustments

# Define color range in HSV
HSV_LOWER = np.array([100, 115, 65])
HSV_UPPER = np.array([115, 255, 255])

def track_color_and_center(camera):
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture image")
            break
        
        # Convert to HSV and create a mask
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print("HSV: ", hsv)
        mask = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
        print("Mask: ", mask)

        # Find contours and select the largest one
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            center_x, center_y = x + w // 2, y + h // 2
            
            # Calculate error from the center of the frame
            frame_center_x = frame.shape[1] // 2
            error_x = center_x - frame_center_x
            
            # Control logic based on the position of the contour
            if abs(error_x) > 20:  # If the dot is not horizontally centered
                turn_direction = np.sign(error_x)
                angular_velocity = ANGULAR_VELOCITY * turn_direction
                sc.driveOpenLoop(np.array([0, angular_velocity]))
                print("Moving forward to color!")
            else:
                # Move forward if not at a desired distance
                if w < 60:  # width of the bounding box as a proxy for distance
                    sc.driveOpenLoop(np.array([FORWARD_VELOCITY, 0]))
                else:
                    sc.driveOpenLoop(np.array([0, 0]))  # Stop if approximately centered
                    print("Target centered and at distance.")
                    break
        else:
            print("No color detected.")
            sc.driveOpenLoop(np.array([0, 0]))  # Stop if no color detected

        sleep(0.1)  # Adjust sleep time based on your specific hardware capabilities

# Usage example assuming a camera object
if __name__ == '__main__':
    while(1):
        camera = cv2.VideoCapture(0)
        try:
            track_color_and_center(camera)
        finally:
            camera.release()
            cv2.destroyAllWindows()
            print("Cleaned up camera resources.")
