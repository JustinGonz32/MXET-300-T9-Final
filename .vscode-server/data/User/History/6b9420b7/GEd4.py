import L1_log as log
import L2_inverse_kinematics as ik
import L2_speed_control as sc
import numpy as np
from time import sleep

# Define some variables for the shapes
pi = np.pi*1.019108  # Utilize the numpy library to define pi
forward_velocity = 0.25  # Forward velocity (x dot) in m/s of SCUTTLE. Note that the max forward velocity of SCUTTLE is 0.4 m/s

# Define the motions for the S shape
motions_s_shape = [
    [forward_velocity, 0, 2],  # Motion 1
    [0, 0.5*pi, 1],             # Motion 2
    [forward_velocity, 0, 3],  # Motion 3
    [0, 0.5*pi, 1],             # Motion 4
    [forward_velocity, 0, 2],  # Motion 5
    [0, -0.5*pi, 1],            # Motion 6
    [forward_velocity, 0, 3],  # Motion 7
    [0, -0.5*pi, 1],            # Motion 8
    [forward_velocity, 0, 2],  # Motion 9
    [0, 0.0, 1],                # Motion 10
]

# Define the motions for the star shape
motions_star_shape = [
    [forward_velocity, 0.2*pi, 2],  # Motion 1
    [0, 0.5*pi, 1],                  # Motion 2
    [forward_velocity, 0, 1],       # Motion 3
    [0, 0.5*pi, 1],                  # Motion 4
    [forward_velocity, 0.2*pi, 2],  # Motion 5
    [0, 0.5*pi, 1],                  # Motion 6
    [forward_velocity, 0, 1],       # Motion 7
    [0, 0.5*pi, 1],                  # Motion 8
    [forward_velocity, 0.2*pi, 2],  # Motion 9
    [0, 0.0, 1],                     # Motion 10
]

# Get user input for the shape selection
shape = input("Enter 'S' for S shape or 'star' for star shape: ")

# Check the user input and execute the corresponding motion sequence
if shape.lower() == 's':
    motions = motions_s_shape
elif shape.lower() == 'star':
    motions = motions_star_shape
else:
    print("Invalid shape selection. Please enter 'S' or 'star'.")
    exit()

# Iterate through and perform each motion and then wait the specified duration.
for count, motion in enumerate(motions):
    print("Motion: ", count+1, "\t Chassis Forward Velocity (m/s): {:.2f} \t Chassis Angular Velocity (rad/s): {:.2f} \t Duration (sec): {:.2f}".format(motion[0], motion[1], motion[2]))
    wheel_speeds = ik.getPdTargets(motion[:2])  # Calculate wheel speeds using inverse kinematics
    sc.driveOpenLoop(wheel_speeds)  # Drive the motors with the calculated wheel speeds
    log.tmpFile(motion[1],"fVel")  # Log forward velocity
    log.tmpFile(motion[2],"aVel")  # Log angular velocity
    sleep(motion[2])  # Wait for the motion duration
