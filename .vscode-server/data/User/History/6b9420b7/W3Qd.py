import L1_log as log
import L2_inverse_kinematics as ik
import L2_speed_control as sc
import numpy as np
from time import sleep
import nodeRedShape
import shapeMotions

# Main function to prompt user input and draw the desired shape
def main():
    while(1):
        #scale_factor = float(input("Enter scale factor (0.1 for small, 1.0 for normal, 2.0 for large): "))
        scale_factor = 1
        shape = nodeRedShape.imageSelectionThread()
        #shape = str(input("Enter shape selection (star, s, square, triangle, or circle): "))
        if shape.lower() == 'star':
            shapeMotions.draw_star(scale_factor)
        elif shape.lower() == 's':
            shapeMotions.draw_s_shape(scale_factor)
        elif shape.lower() == 'square':
            shapeMotions.draw_square(scale_factor)
        elif shape.lower() == 'triangle':
            shapeMotions.draw_triangle(scale_factor)
        elif shape.lower() == 'circle':
            shapeMotions.draw_circle(scale_factor)                
        else:
            print("Invalid input. Please enter either 'star', 's', or 'square'.")

if __name__ == "__main__":
    main()
