import L1_log as log
import L2_inverse_kinematics as ik
import L2_speed_control as sc
import numpy as np
from time import sleep
import nodeRedShape

import shapeMotions

# Main function to prompt user input and draw the desired shape
def main():
    nodeRedShape.shapeSelectionThread.isAlive()
    while(1):
        #scale_factor = float(input("Enter scale factor (0.1 for small, 1.0 for normal, 2.0 for large): "))
        scale_factor = 1
        shape = str(nodeRedShape.selected_shape)
        #shape = str(input("Enter shape selection (star, s, square, triangle, or circle): "))
        #print("In shape selecting loop!")
        if shape.strip() == 'star':
            shapeMotions.draw_star(scale_factor)
        elif shape.strip() == 's_shape':
            shapeMotions.draw_s_shape(scale_factor)
        elif shape.strip() == 'square':
            shapeMotions.draw_square(scale_factor)
        elif shape.strip() == 'triangle':
            print("In Triangle loop")
            shapeMotions.draw_triangle(scale_factor)
            nodeRedShape.selected_shape = ""
        elif shape.strip() == 'circle':
            shapeMotions.draw_circle(scale_factor)                
        else:
            continue
            #print("Invalid input. Please enter either 'star', 's', or 'square'.")

if __name__ == "__main__":
    main()
