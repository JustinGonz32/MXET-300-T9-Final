import numpy as np
import L2_speed_control as sc
import L2_inverse_kinematics as ik
import L2_vector as lidar
import L1_log as log
from time import sleep
import cv2
import netifaces as ni
import sys

# define some variables that can be used to create the path
# make use of these definitions in the motions list
pi = np.pi*1.019108                  # utilize the numpy library to define pi
d1 = 0.5                      # distance in meters of segment 1 in the path
d2 = 0.75                      # distance in meters of segment 2 in the path
forward_velocity = 0.25      # forward velocity (x dot) in m/s of SCUTTLE. NOTE that the max forward velocity of SCUTTLE is 0.4 m/s

size_w  = 240   # Resized image width. This is the image width in pixels.
size_h = 160	# Resized image height. This is the image height in pixels.

fov = 1         # Camera field of view in rad (estimate)
#    Color Range, described in HSV
v1_min = 0      # Minimum H value
v2_min = 110     # Minimum S value
v3_min = 215      # Minimum V value

v1_max = 20     # Maximum H value
v2_max = 225    # Maximum S value
v3_max = 255    # Maximum V value

target_width = 100      # Target pixel width of tracked object
angle_margin = 0.2      # Radians object can be from image center to be considered "centered"
width_margin = 20       # Minimum width error to drive forward/back


# below is a list setup to run through each motion segment to create the path.
# the list elements within each list are in order as follows: chassis forward velocity (m/s), chassis angular velocity (rad/s), and motion duration (sec)
# enter the chassis forward velocity (x dot) in m/s, chassis angular velocity (theta dot) in rad/s, and motion duration in sec for each motion to create the path
motions1 = [
    [0.25, 0, 1]            # Motion 1 forward (veloctiy, angle, time sec) 
]

motions2 = [
    [0, 0.5*pi, 1.3],            # Motion 1 right turn (veloctiy, angle, time sec)
    [1, 0, 2],            # Motion 1 forward (veloctiy, angle, time sec)
    [0, -0.5*pi, 1.3],
    [1, 0, 2]            # Motion 1 right turn (veloctiy, angle, time sec)
]

def executeMotions(motions):
    for  count, motion in enumerate(motions):
                print("Motion: ", count+1, "\t Chassis Forward Velocity (m/s): {:.2f} \t Chassis Angular Velocity (rad/s): {:.2f} \t Duration (sec): {:.2f}".format(motion[0], motion[1], motion[2]))
                wheel_speeds = ik.getPdTargets(motion[:2])                  # take the forward speed(m/s) and turning speed(rad/s) and use inverse kinematics to deterimine wheel speeds
                sc.driveOpenLoop(wheel_speeds)                              # take the calculated wheel speeds and use them to run the motors
                sleep(motion[2])
class ColorTracker:
    def __init__(self):
        self.stream_ip = self.get_ip()
        if not self.stream_ip:
            raise Exception("Failed to get IP for camera stream")
        self.camera_input = 'http://' + self.stream_ip + ':8090/?action=stream'
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
        camera = cv2.VideoCapture(self.camera_input)
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

                if len(cnts) > 0:
                    self.process_contours(cnts, image.shape[1])

        except KeyboardInterrupt:
            print("Color tracking stopped by user.")

        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            print("Camera resources released.")

    def check_for_target(self):
        ret, image = self.camera.read()
        if not ret:
            print("Failed to retrieve image!")
            return False

        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(image, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        return len(cnts) > 0  # Returns True if contours are found, indicating presence of the target
    
    def process_contours(self, cnts, frame_width):
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        center = (int(x + 0.5 * w), int(y + 0.5 * h))
        angle = round(((center[0] / frame_width) - 0.5) * self.fov, 3)

        if abs(angle) < self.angle_margin:
            self.align_and_approach_target(angle, w)
        else:
            self.adjust_heading(angle)

    def align_and_approach_target(self, angle, contour_width):
        e_width = self.target_width - contour_width
        if abs(e_width) < self.width_margin:
            sc.driveOpenLoop(np.array([0., 0.]))
            print("Aligned! Width:", contour_width)
            sys.exit()
            return
        
        fwd_effort = e_width / self.target_width
        wheel_speed = ik.getPdTargets(np.array([0.8 * fwd_effort, -0.5 * angle]))
        sc.driveOpenLoop(wheel_speed)
        print(f"Approaching target. Angle: {angle}, Target L/R: {wheel_speed}")

    def adjust_heading(self, angle):
        wheel_speed = ik.getPdTargets(np.array([0, -1.1 * angle]))
        sc.driveOpenLoop(wheel_speed)
        print(f"Adjusting heading. Angle: {angle}, Target L/R: {wheel_speed}")

##################################################
def main():
    detect_obj = False
    while detect_obj == False:  #While nothing is detected
        closePoint = lidar.getNearest() #acesses lidar data (radius meters, angle degrees)
        if closePoint[0] <= 0.3: #object IS close to robot currently 
            detect_obj = True
        if closePoint[0] > 0.3: #object IS NOT close to robot currently 
            # iterate through and perform each open loop motion and then wait the specified duration.
            executeMotions(motions1)                       # wait the motion duration
            detect_obj = False
    executeMotions(motions2)
    tracker = ColorTracker()
    tracker.track_color()
##################################################


    
#print("main loop exited")
            

if __name__ == "__main__":
    main()


