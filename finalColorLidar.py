import cv2
import numpy as np
import L2_speed_control as sc
import L2_inverse_kinematics as ik
import L2_kinematics as kin
import L2_vector as lidar
import netifaces as ni
from time import sleep
from math import radians
import sys

class ColorTracker:
    def __init__(self):
        self.stream_ip = self.get_ip()
        if not self.stream_ip:
            raise Exception("Failed to get IP for camera stream")

        self.size_w = 240
        self.size_h = 160
        self.camera_input = f'http://{self.stream_ip}:8090/?action=stream'
        self.camera = self.setup_camera()

        self.fov = radians(60)  # Field of view per increment
        self.v1_min, self.v2_min, self.v3_min = 100, 115, 65
        self.v1_max, self.v2_max, self.v3_max = 115, 255, 255
        self.target_width = 125
        self.angle_margin = radians(20)
        self.width_margin = 10

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
        try:
            while True:
                ret, image = self.camera.read()
                if not ret:
                    print("Failed to retrieve image!")
                    continue

                image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                thresh = cv2.inRange(image_hsv, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
                if cv2.countNonZero(thresh) > 0:
                    self.process_image(image_hsv)
                else:
                    self.spin_360()

        except KeyboardInterrupt:
            print("Color tracking stopped by user.")
        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            print("Camera resources released.")

    def process_image(self, hsv_image):
        thresh = cv2.inRange(hsv_image, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
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
        cart = lidar.polar2cart(closePoint[0],closePoint[1])
        e_width = self.target_width - width

        if ((abs(width_error) < self.width_margin) and (abs(angle_error) < self.angle_margin)):
            sc.driveOpenLoop(np.array([0, 0]))
            print("Target aligned and approached.")
        else:
            if(cart[1] < (self.width_margin - 9.8)):
                correction_speed = ik.getPdTargets(np.array([0.5 * (width_error / self.target_width), -angle_error]))
                sc.driveOpenLoop(correction_speed)
                print("Adjusting to target...")
            else:
                print("Close enuf")
                print("cart1: ",cart[1])
                sys.exit()

    def spin_360(self):
        print("Scanning for target...")
        for _ in range(6):  # Spin in 60-degree increments
            sc.driveOpenLoop(np.array([4, -4]))  # Simple rotation command
            sleep(.33)  # Spin for a time to cover 60 degrees
            sc.driveOpenLoop(np.array([0, 0]))  # Stop to scan
            sleep(1)  # Wait for the camera image to stabilize
            ret, image = self.camera.read()
            if ret:
                image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                thresh = cv2.inRange(image_hsv, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
                if cv2.countNonZero(thresh) > 0:
                    print("Target detected during spin.")
                    self.process_image(image_hsv)
                    break  # Exit the spin loop if the target is found

if __name__ == '__main__':
    tracker = ColorTracker()
    tracker.track_color()
