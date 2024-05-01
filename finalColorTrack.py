import cv2
import numpy as np
import L2_speed_control as sc
import L2_inverse_kinematics as ik
import L2_kinematics as kin
import netifaces as ni
from time import sleep
from math import radians, pi

class ColorTracker:
    def __init__(self):
        self.stream_ip = self.get_ip()
        if not self.stream_ip:
            raise Exception("Failed to get IP for camera stream")

        self.camera_input = 'http://' + self.stream_ip + ':8090/?action=stream'  # Correct use of self.stream_ip
        self.size_w = 240
        self.size_h = 160
        self.fov = 1
        self.v1_min, self.v2_min, self.v3_min = 100, 115, 65
        self.v1_max, self.v2_max, self.v3_max = 115, 225, 255
        self.target_width = 100
        self.angle_margin = 0.2
        self.width_margin = 10

        self.camera = self.setup_camera()

    def get_ip(self):
        for interface in ni.interfaces()[1:]:
            try:
                ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
                return ip
            except KeyError:
                continue
        return 0

    def setup_camera(self):
        camera = cv2.VideoCapture(self.camera_input)  # Use self.camera_input correctly
        if not camera.isOpened():
            camera = cv2.VideoCapture(0)
        camera.set(3, self.size_w)
        camera.set(4, self.size_h)
        return camera

    def track_color(self):
        try:
            while True:
                sleep(.05)
                ret, image = self.camera.read()
                if not ret:
                    print("Failed to retrieve image!")
                    break

                image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                thresh = cv2.inRange(image, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                if len(cnts) and len(cnts) < 3:
                    self.process_contours(cnts, image.shape[1])

        except KeyboardInterrupt:
            print("Color tracking stopped by user.")

        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            print("Camera resources released.")

    def process_contours(self, cnts, frame_width):
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        center = (int(x + 0.5 * w), int(y + 0.5 * h))
        angle = round(((center[0] / frame_width) - 0.5) * self.fov, 3)

        wheel_measured = kin.getPdCurrent()
        if abs(angle) < self.angle_margin:
            self.align_and_approach_target(angle, w)
        else:
            self.adjust_heading(angle)

    def align_and_approach_target(self, angle, contour_width):
        e_width = self.target_width - contour_width
        if abs(e_width) < self.width_margin:
            sc.driveOpenLoop(np.array([0., 0.]))  # Stop the SCUTTLE if it's well aligned
            print("Aligned! Width:", contour_width)
            return

        # Calculate the forward drive effort based on width error
        fwd_effort = e_width / self.target_width
        # Calculate wheel speeds: proportional to forward effort and adjusted for angle
        wheel_speed = ik.getPdTargets(np.array([0.8 * fwd_effort, -0.5 * angle]))

        # Retrieve current wheel speeds for closed loop control
        wheel_measured = kin.getPdCurrent()

        # Implement Closed Loop control if desired, or Open Loop for testing
        #sc.driveClosedLoop(wheel_speed, wheel_measured, np.zeros(2))  # Assuming zero derivative error
        sc.driveOpenLoop(wheel_speed)
        print(f"Approaching target. Angle: {angle}, Target L/R: {wheel_speed}, Measured L/R: {wheel_measured}")

    def adjust_heading(self, angle):
        # Calculate wheel speeds needed for turning: negative for left turn correction
        wheel_speed = ik.getPdTargets(np.array([0, -1.1 * angle]))

        # Retrieve current wheel speeds for closed loop control
        wheel_measured = kin.getPdCurrent()

        # Implement Closed Loop control if desired, or Open Loop for testing
        #sc.driveClosedLoop(wheel_speed, wheel_measured, np.zeros(2))  # Assuming zero derivative error
        sc.driveOpenLoop(wheel_speed)
        print(f"Adjusting heading. Angle: {angle}, Target L/R: {wheel_speed}, Measured L/R: {wheel_measured}")


# For direct running of the script
if __name__ == '__main__':
    tracker = ColorTracker()
    tracker.track_color()
