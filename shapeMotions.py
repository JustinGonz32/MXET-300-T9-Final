import numpy as np
import L2_inverse_kinematics as ik
import L2_kinematics as kin
import L2_speed_control as sc
import L1_log as log
from time import sleep
import nodeRedShape
import servo
import L2_vector
import finalColorTrack
#import math

# Define constants for the shapes
pi = np.pi * 1.019108  # Define pi using numpy
forward_velocity = 0.25  # Forward velocity (x dot) in m/s of SCUTTLE
quarter_turn = 0.5 * pi  # Quarter turn in radians
third_turn = 0.75 * pi  # Quarter turn in radians
half_turn = pi  # Half turn in radians
full_turn = 2 * pi  # Full turn in radians
side_length = 0.5  # Side length of the square

# Define closed loop controls
count = 0 # number of loop iterations
# INITIALIZE VARIABLES FOR CONTROL SYSTEM
t0 = 0  # time sample
t1 = 1  # time sample
e00 = 0 # error sample
e0 = 0  # error sample
e1 = 0  # error sample
dt = 0  # delta in time
de_dt = np.zeros(2)
scale_factor = 1

# Function to draw a star shape
def draw_star(scale_factor, mode):
    forward_motion_duration = 2  # Constant forward motion duration
    angular_rotation_duration = 1  # Constant angular rotation duration
    motions = [
        [forward_velocity * scale_factor, 0, forward_motion_duration],  # Motion 1: Move forward
        [0, quarter_turn, angular_rotation_duration],  # Motion 2: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, forward_motion_duration],  # Motion 3: Move forward
        [0, -half_turn, angular_rotation_duration],  # Motion 4: Rotate a half turn
        [forward_velocity * scale_factor, 0, forward_motion_duration],  # Motion 5: Move forward
        [0, quarter_turn, angular_rotation_duration],  # Motion 6: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, forward_motion_duration],  # Motion 7: Move forward
        [0, -half_turn, angular_rotation_duration],  # Motion 8: Rotate a half turn
        [forward_velocity * scale_factor, 0, forward_motion_duration],  # Motion 9: Move forward
        [0, quarter_turn, angular_rotation_duration],  # Motion 10: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, forward_motion_duration],  # Motion 11: Move forward
        [0, -half_turn, angular_rotation_duration],  # Motion 12: Rotate a half turn
        [0, 0, 1]  # Motion 13: Stop
    ]
    if (mode == 'open'):
        execute_motions(motions)
    elif(mode == 'closed'):
        #Convert pdt and pdc to NumPy arrays
        pdt = np.array([0, 0])  # Stop command (zero speed)
        pdc = np.array([0, 0])  # Zero current speeds
        # Execute motions using closed-loop control
        execute_motions_cl(motions, pdt, pdc)

# Function to draw an S shape
def draw_s_shape(scale_factor, mode):
    forward_motion_duration = 2 * scale_factor  # Adjust the forward motion duration based on the scale factor
    angular_rotation_duration = 1 * scale_factor  # Adjust the angular rotation duration based on the scale factor
    motions = [
        [forward_velocity, 0, forward_motion_duration],  # Motion 1: Move forward
        [0, quarter_turn, angular_rotation_duration],  # Motion 2: Rotate a quarter turn
        [forward_velocity, 0, 3 * scale_factor],  # Motion 3: Move forward
        [0, quarter_turn, angular_rotation_duration],  # Motion 4: Rotate a quarter turn
        [forward_velocity, 0, forward_motion_duration],  # Motion 5: Move forward
        [0, -quarter_turn, angular_rotation_duration],  # Motion 6: Rotate a quarter turn
        [forward_velocity, 0, 3 * scale_factor],  # Motion 7: Move forward
        [0, -quarter_turn, angular_rotation_duration],  # Motion 8: Rotate a quarter turn
        [forward_velocity, 0, forward_motion_duration],  # Motion 9: Move forward
        [0, half_turn, angular_rotation_duration],  # Motion 10: Rotate a half turn
        [0, 0, 1]  # Motion 11: Stop
    ]
    if (mode == 'open'):
        execute_motions(motions)
    elif(mode == 'closed'):
        #Convert pdt and pdc to NumPy arrays
        pdt = np.array([0, 0])  # Stop command (zero speed)
        pdc = np.array([0, 0])  # Zero current speeds
        # Execute motions using closed-loop control
        execute_motions_cl(motions, pdt, pdc)

# Function to draw a square shape
def draw_square(scale_factor, mode):
    forward_motion_duration = side_length / forward_velocity  # Calculate the forward motion duration based on the side length
    angular_rotation_duration = 1  # Constant angular rotation duration
    motions = [
        [forward_velocity, 0, forward_motion_duration],  # Motion 1: Move forward
        [0, -quarter_turn, angular_rotation_duration * scale_factor],  # Motion 2: Rotate a quarter turn
        [forward_velocity, 0, forward_motion_duration],  # Motion 3: Move forward
        [0, -quarter_turn, angular_rotation_duration * scale_factor],  # Motion 4: Rotate a quarter turn
        [forward_velocity, 0, forward_motion_duration],  # Motion 5: Move forward
        [0, -quarter_turn, angular_rotation_duration * scale_factor],  # Motion 6: Rotate a quarter turn
        [forward_velocity, 0, forward_motion_duration],  # Motion 7: Move forward
        [0, -quarter_turn, angular_rotation_duration * scale_factor],  # Motion 8: Rotate a quarter turn
        [0, 0, 1]  # Motion 9: Stop
    ]
    if (mode == 'open'):
        execute_motions(motions)
    elif(mode == 'closed'):
        #Convert pdt and pdc to NumPy arrays
        pdt = np.array([0, 0])  # Stop command (zero speed)
        pdc = np.array([0, 0])  # Zero current speeds
        # Execute motions using closed-loop control
        execute_motions_cl(motions, pdt, pdc)

def draw_triangle(scale_factor, mode):
    # Define the sequence of motions to draw a triangle
    motions = [
        [forward_velocity, 0, 2],        # Motion 1: Move forward
        [0, third_turn, 2],                      # Motion 2: Rotate 120 degrees (1/3 of a full circle)
        [forward_velocity, 0, 2],        # Motion 3: Move forward
        [0, third_turn, 2],                      # Motion 4: Rotate 120 degrees (1/3 of a full circle)
        [forward_velocity, 0, 2],        # Motion 5: Move forward
        [0, third_turn, 2],                      # Motion 6: Rotate 120 degrees (1/3 of a full circle)
        [0, 0, 1]  # Motion 9: Stop
    ]
    if (mode == 'open'):
        execute_motions(motions)
    elif(mode == 'closed'):
        #Convert pdt and pdc to NumPy arrays
        pdt = np.array([0, 0])  # Stop command (zero speed)
        pdc = np.array([0, 0])  # Zero current speeds
        # Execute motions using closed-loop control
        execute_motions_cl(motions, pdt, pdc)

def draw_square(scale_factor, mode):
    # Define the sequence of motions to draw a square
    motions = [
        [forward_velocity, 0, 2],        # Motion 1: Move forward
        [0, 90, 1],                       # Motion 2: Rotate 90 degrees (quarter turn)
        [forward_velocity, 0, 2],        # Motion 3: Move forward
        [0, 90, 1],                       # Motion 4: Rotate 90 degrees (quarter turn)
        [forward_velocity, 0, 2],        # Motion 5: Move forward
        [0, 90, 1],                       # Motion 6: Rotate 90 degrees (quarter turn)
        [forward_velocity, 0, 2],        # Motion 7: Move forward
        [0, 90, 1],                       # Motion 8: Rotate 90 degrees (quarter turn)
        [0, 0, 1]  # Motion 9: Stop
    ]
    if (mode == 'open'):
        execute_motions(motions)
    elif(mode == 'closed'):
        #Convert pdt and pdc to NumPy arrays
        pdt = np.array([0, 0])  # Stop command (zero speed)
        pdc = np.array([0, 0])  # Zero current speeds
        # Execute motions using closed-loop control
        execute_motions_cl(motions, pdt, pdc)

def draw_circle(scale, mode):
    # Define parameters for drawing the circle
    radius = 0.5  # Radius of the circle in meters
    num_segments = 36  # Number of line segments to approximate the circle
    motion_duration = 0.5  # Duration of each motion segment in seconds

    # Calculate the angle increment between each line segment
    angle_increment = 2 * pi / num_segments

    # Define the sequence of motions to draw the circle
    motions = []
    for _ in range(num_segments):
        motions.append([forward_velocity, angle_increment, motion_duration])
    motions.append([0, 0, 1])
    if (mode == 'open'):
        execute_motions(motions)
    elif(mode == 'closed'):
        #Convert pdt and pdc to NumPy arrays
        pdt = np.array([0, 0])  # Stop command (zero speed)
        pdc = np.array([0, 0])  # Zero current speeds
        # Execute motions using closed-loop control
        execute_motions(motions, pdt, pdc)


# Function to execute motions with closed-loop control
def execute_motions_cl(motions, pdt, pdc):
    for count, motion in enumerate(motions):
        print("Motion: ", count+1, "\t Chassis Forward Velocity (m/s): {:.2f} \t Chassis Angular Velocity (rad/s): {:.2f} \t Duration (sec): {:.2f}".format(motion[0], motion[1], motion[2]))
        wheel_speeds = ik.getPdTargets(motion[:2])
        sc.driveClosedLoop(wheel_speeds, pdt, pdc)  # Use driveClosedLoop for closed-loop control                           
        #log.tmpFile(motion[1],"fVel") 
        #log.tmpFile(motion[2],"aVel") 
        sleep(motion[2])
    nodeRedShape.selected_shape = ""

# Function to execute motions with closed-loop control
def execute_motions(motions):
    motion_0()
    servo.servoInt()
    servo.set_angle(-90)
    sleep(0.1)
    servo.servoInt()
    sleep(1)
    for  count, motions in enumerate(motions):
        print("Motion: ", count+1, "\t Chassis Forward Velocity (m/s): {:.2f} \t Chassis Angular Velocity (rad/s): {:.2f} \t Duration (sec): {:.2f}".format(motions[0], motions[1], motions[2]))
        wheel_speeds = ik.getPdTargets(motions[:2])                  # take the forward speed(m/s) and turning speed(rad/s) and use inverse kinematics to deterimine wheel speeds
        sc.driveOpenLoop(wheel_speeds)                              # take the calculated wheel speeds and use them to run the motors
        #log.tmpFile(motion[1],"fVel") #Log forward velocity
        #log.tmpFile(motion[2],"aVel") #Log angular velocity
        sleep(motions[2])
    servo.set_angle(90)
    sleep(0.1)
    servo.servoInt()
    nodeRedShape.selected_shape = ""

def motion_0():
    #servo.set_angle()
    sleep(0.1)
    servo.servoInt()
    ini_mot = [forward_velocity, 0, 1]
    wheel_speeds = ik.getPdTargets(ini_mot[:2])
    print("Wheel speeds: ", wheel_speeds)
    sc.driveOpenLoop(wheel_speeds)  # Use openLoop
    print("Scale factor: ", scale_factor)
    sleep(ini_mot[2])  # Adjusted to use ini_mot[2] instead of motion[2]
    #log.tmpFile(ini_mot[1], "fVel") 
    #log.tmpFile(ini_mot[2], "aVel")
    ini_mot = [0, 0, 1]
    wheel_speeds = ik.getPdTargets(ini_mot[:2])
    sc.driveOpenLoop(wheel_speeds)
    sleep(ini_mot[2])

def obsAvoid():
    posData = L2_vector.getNearest()
    cart = L2_vector.polar2cart(data[0],data[1])
    if(cart[0] > 0.5):
        motions_avoid = [
        [0, quarter_turn, angular_rotation_duration],  # Motion 2: Rotate a quarter turn
        [forward_velocity, 0, 3 * scale_factor],  # Motion 3: Move forward
        [0, quarter_turn, angular_rotation_duration],  # Motion 4: Rotate a quarter turn
        [forward_velocity, 0, forward_motion_duration],  # Motion 5: Move forward
        [0, -quarter_turn, angular_rotation_duration],  # Motion 6: Rotate a quarter turn
        [forward_velocity, 0, 3 * scale_factor],  # Motion 7: Move forward
        [0, 0, 1] #Stop
        ]
        execute_motions(motions_avoid)
    else:
        pass

def colorTrack():
    tracker = finalColorTrack.ColorTracker()
    tracker.track_color()

def botOrgin():
    while(finalColorTrack.)

def main():
    while(1):
        #shape = nodeRedShape.selected_shape
        servo.servoInt()
        colorTrack()
        obsAvoid()
        shape = input("Shape: ")
        mode = input("Closed or open loop: ")
        scale = 1
        print("Motions - Shape: ", shape)

        if (shape == ' circle'):
            print("In circle!")
            draw_circle(scale,mode)
        elif (shape == ' square'):
            draw_square(scale, mode)
        elif(shape == ' triangle'):
            draw_triangle(scale,mode)
        elif(shape == ' s-shape'):
            draw_s_shape(scale,mode)
        elif(shape == 'mxet'):
            draw_m
            draw_x
            draw_e
            draw_t
        else:
            print("Bad Read, womp womp")


if __name__ == "__main__":   
    main()
