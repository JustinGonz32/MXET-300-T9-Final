import cv2
import numpy as np
import L2_speed_control as sc
import L2_inverse_kinematics as ik
import L2_vector as lidar
import netifaces as ni
from time import sleep
from math import radians

class ColorTracker:
    def __init__(self):
        self.stream_ip = self.get_ip()
        if not self.stream_ip:
            raise Exception("Failed to get IP for camera stream")

        self.size_w = 240
        self.size_h = 160
        self.camera_input = f'http://{self.stream_ip}:8090/?action=stream'
        self.camera = self.setup_camera()

        self.fov = radians(60)
        self.v1_min, self.v2_min, self.v3_min = 60, 140, 50
        self.v1_max, self.v2_max, self.v3_max = 155, 255, 255
        self.target_width = 125
        self.angle_margin = radians(20)
        self.width_margin = 10

        self.state = "SEARCHING"

    def get_ip(self):
        for interface in ni.interfaces()[1:]:
            try:
                ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
                return ip
            except KeyError:
                continue
        return None

    def setup_camera(self):
        camera = cv2.VideoCapture(self.camera_input)
        if not camera.isOpened():
            camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.size_w)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.size_h)
        return camera

    def track_color(self):
        while True:
            ret, image = self.camera.read()
            if not ret:
                print("Failed to retrieve image!")
                continue

            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            target_mask = cv2.inRange(image_hsv, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
            blue_detected = cv2.countNonZero(target_mask) > 0

            if self.state == "SEARCHING":
                if blue_detected:
                    self.state = "APPROACHING"
                else:
                    sc.driveOpenLoop(np.array([5, 5]))  # Keep searching

            elif self.state == "APPROACHING":
                if blue_detected:
                    self.process_image(image_hsv)  # Process to move towards the target
                else:
                    self.state = "SEARCHING"  # Target lost, go back to searching

            elif self.state == "AVOIDING":
                sc.driveOpenLoop(np.array([5, -5]))  # Simple avoidance maneuver
                sleep(0.5)  # Turn for a bit
                self.state = "SEARCHING"  # Return to searching after avoiding

    def process_image(self, hsv_image):
        self.current_hsv_image = hsv_image  # Store the HSV image for use in alignment
        target_mask = cv2.inRange(hsv_image, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
        
        mask = cv2.morphologyEx(target_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            c = max(cnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            self.align_and_approach_target(x + w // 2, w)

    def align_and_approach_target(self, center_x, width):
        frame_center = self.size_w // 2
        angle_error = ((center_x - frame_center) / frame_center) * self.fov
        width_error = self.target_width - width

        closePoint = lidar.getNearest()
        if closePoint is not None and closePoint[0] < 0.3:  # General obstacle detection
            if self.state != "APPROACHING":
                print("Obstacle detected, avoiding...")
                self.avoid_obstacle()
            else:
                print("Target detected, approaching...")
                self.approach_target(center_x, width_error, angle_error)
        else:
            print("No close obstacle detected. Moving forward...")
            sc.driveOpenLoop(np.array([8, 8]))  # Keep moving forward if no close obstacle
            self.state = "SEARCHING"

    def avoid_obstacle(self):
        # Stop the robot first
        sc.driveOpenLoop(np.array([0, 0]))
        sleep(0.2)  # Brief pause
        # Make a right turn
        sc.driveOpenLoop(np.array([8, -8]))
        sleep(0.5)  # Turn for a bit
        # Move forward to ensure it clears the obstacle
        sc.driveOpenLoop(np.array([8, 8]))
        sleep(1.5)  # Move forward after the turn
        # Return to searching after moving forward enough to potentially clear the obstacle
        self.state = "SEARCHING"

    def approach_target(self, center_x, width_error, angle_error):
        correction_speed = ik.getPdTargets(np.array([0.5 * (width_error / self.target_width), -angle_error]))
        sc.driveOpenLoop(correction_speed)
        # If needed, implement logic to switch to 'SEARCHING' if the target is lost or reached

if __name__ == '__main__':
    tracker = ColorTracker()
    tracker.track_color()
    