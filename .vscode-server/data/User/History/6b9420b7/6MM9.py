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
side_length = 0.5  # Side length of the square

# Function to draw a star shape
def draw_star(scale_factor):
    motions = [
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 1: Move forward
        [0, quarter_turn, 1 * scale_factor],             # Motion 2: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 3: Move forward
        [0, -half_turn, 1 * scale_factor],               # Motion 4: Rotate a half turn
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 5: Move forward
        [0, quarter_turn, 1 * scale_factor],             # Motion 6: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 7: Move forward
        [0, -half_turn, 1 * scale_factor],               # Motion 8: Rotate a half turn
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 9: Move forward
        [0, quarter_turn, 1 * scale_factor],             # Motion 10: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 11: Move forward
        [0, -half_turn, 1 * scale_factor],               # Motion 12: Rotate a half turn
        [0, 0, 1 * scale_factor]                          # Motion 13: Stop
    ]
    execute_motions(motions)

# Function to draw an S shape
def draw_s_shape(scale_factor):
    motions = [
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 1: Move forward
        [0, quarter_turn, 1 * scale_factor],             # Motion 2: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, 3 * scale_factor],        # Motion 3: Move forward
        [0, quarter_turn, 1 * scale_factor],             # Motion 4: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 5: Move forward
        [0, -quarter_turn, 1 * scale_factor],            # Motion 6: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, 3 * scale_factor],        # Motion 7: Move forward
        [0, -quarter_turn, 1 * scale_factor],            # Motion 8: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, 2 * scale_factor],        # Motion 9: Move forward
        [0, half_turn, 1 * scale_factor],                # Motion 10: Rotate a half turn
        [0, 0, 1 * scale_factor]                          # Motion 11: Stop
    ]
    execute_motions(motions)

# Function to draw a square shape
def draw_square(scale_factor):
    motions = [
        [forward_velocity * scale_factor, 0, side_length * scale_factor],        # Motion 1: Move forward
        [0, -quarter_turn, 1 * scale_factor],             # Motion 2: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, side_length * scale_factor],        # Motion 3: Move forward
        [0, -quarter_turn, 1 * scale_factor],             # Motion 4: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, side_length * scale_factor],        # Motion 5: Move forward
        [0, -quarter_turn, 1 * scale_factor],             # Motion 6: Rotate a quarter turn
        [forward_velocity * scale_factor, 0, side_length * scale_factor],        # Motion 7: Move forward
        [0, -quarter_turn, 1 * scale_factor],             # Motion 8: Rotate a quarter turn
        [0, 0, 1 * scale_factor]                          # Motion 9: Stop
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
    while(1):
        scale_factor = float(input("Enter scale factor (0.1 for small, 1.0 for normal, 2.0 for large): "))
        shape = input("Enter 'star' to draw a star shape, 's' to draw an S shape, or 'square' to draw a square: ")
        if shape.lower() == 'star':
            draw_star(scale_factor)
        elif shape.lower() == 's':
            draw_s_shape(scale_factor)
        elif shape.lower() == 'square':
            draw_square(scale_factor)
        else:
            print("Invalid input. Please enter either 'star', 's', or 'square'.")

if __name__ == "__main__":
    main()
