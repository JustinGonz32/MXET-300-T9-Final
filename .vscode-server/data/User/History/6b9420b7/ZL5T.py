import L1_log as log
import L2_inverse_kinematics as ik
import L2_speed_control as sc
import numpy as np
from time import sleep

# Define constants for the shapes
pi = np.pi * 1.019108  # Define pi using numpy
forward_velocity = 0.25  # Forward velocity (x dot) in m/s of SCUTTLE
quarter_turn = 0.5 * pi  # Quarter turn in radians
half_turn = pi  # Half turn in radians
full_turn = 2 * pi  # Full turn in radians

# Function to draw a star shape
def draw_star():
    motions = [
        [forward_velocity, 0, 2],        # Motion 1: Move forward
        [0, quarter_turn, 1],             # Motion 2: Rotate a quarter turn
        [forward_velocity, 0, 2],        # Motion 3: Move forward
        [0, -half_turn, 1],               # Motion 4: Rotate a half turn
        [forward_velocity, 0, 2],        # Motion 5: Move forward
        [0, quarter_turn, 1],             # Motion 6: Rotate a quarter turn
        [forward_velocity, 0, 2],        # Motion 7: Move forward
        [0, -half_turn, 1],               # Motion 8: Rotate a half turn
        [forward_velocity, 0, 2],        # Motion 9: Move forward
        [0, quarter_turn, 1],             # Motion 10: Rotate a quarter turn
        [forward_velocity, 0, 2],        # Motion 11: Move forward
        [0, -half_turn, 1],               # Motion 12: Rotate a half turn
    ]
    execute_motions(motions)

# Function to draw an S shape
def draw_s_shape():
    motions = [
        [forward_velocity, 0, 2],        # Motion 1: Move forward
        [0, quarter_turn, 1],             # Motion 2: Rotate a quarter turn
        [forward_velocity, 0, 3],        # Motion 3: Move forward
        [0, quarter_turn, 1],             # Motion 4: Rotate a quarter turn
        [forward_velocity, 0, 2],        # Motion 5: Move forward
        [0, -quarter_turn, 1],            # Motion 6: Rotate a quarter turn
        [forward_velocity, 0, 3],        # Motion 7: Move forward
        [0, -quarter_turn, 1],            # Motion 8: Rotate a quarter turn
        [forward_velocity, 0, 2],        # Motion 9: Move forward
        [0, half_turn, 1],                # Motion 10: Rotate a half turn
    ]
    execute_motions(motions)

# Function to execute motions
def execute_motions(motions):
    for count, motion in enumerate(motions):
        print("Motion: ", count+1, "\t Chassis Forward Velocity (m/s): {:.2f} \t Chassis Angular Velocity (rad/s): {:.2f} \t Duration (sec): {:.2f}".format(motion[0], motion[1], motion[2]))
        wheel_speeds = ik.getPdTargets(motion[:2])                  
        sc.driveOpenLoop(wheel_speeds)                              
        log.tmpFile(motion[1],"fVel") 
        log.tmpFile(motion[2],"aVel") 
        sleep(motion[2])

# Main function to prompt user input and draw the desired shape
def main():
    shape = input("Enter 'star' to draw a star shape or 's' to draw an S shape: ")
    if shape.lower() == 'star':
        draw_star()
    elif shape.lower() == 's':
        draw_s_shape()
    else:
        print("Invalid input. Please enter either 'star' or 's'.")

if __name__ == "__main__":
    main()
