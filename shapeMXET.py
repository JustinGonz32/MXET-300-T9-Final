# Function to draw the letter 'M'
def draw_m(scale_factor, mode):
    side_length = 1.0  # Adjust the side length as necessary
    forward_motion_duration = side_length / forward_velocity
    motions = [
        [forward_velocity, 0, forward_motion_duration],  # Move up the left leg of 'M'
        [0, -quarter_turn, 0.5],  # Turn to start the middle V
        [forward_velocity, 0, forward_motion_duration * 0.5],  # Move up the middle V
        [0, quarter_turn, 0.5],  # Turn to finish the middle V
        [forward_velocity, 0, forward_motion_duration * 0.5],  # Move down the middle V to the center
        [0, quarter_turn, 0.5],  # Start the right leg
        [forward_velocity, 0, forward_motion_duration],  # Move up the right leg of 'M'
        [0, 0, 1]  # Stop motion
    ]
    if (mode == 'open'):
        execute_motions(motions)
    elif(mode == 'closed'):
        #Convert pdt and pdc to NumPy arrays
        pdt = np.array([0, 0])  # Stop command (zero speed)
        pdc = np.array([0, 0])  # Zero current speeds
        # Execute motions using closed-loop control
        execute_motions(motions, pdt, pdc)
    #execute_motions(motions, np.array([0, 0]), np.array([0, 0]))  # Convert pdt and pdc to NumPy arrays for stopping

# Function to draw the letter 'X'
def draw_x(scale_factor):
    forward_motion_duration = np.sqrt(2) * (1.0 / forward_velocity)  # Calculate the hypotenuse for diagonal
    motions = [
        [forward_velocity, 0, forward_motion_duration],  # Move first diagonal of 'X'
        [0, half_turn, 0.5],  # Rotate 180 degrees to go back
        [forward_velocity, 0, forward_motion_duration],  # Complete the X by second diagonal
        [0, quarter_turn, 0.5],  # Rotate to neutral position
        [0, 0, 1]  # Stop motion
    ]
    execute_motions(motions, np.array([0, 0]), np.array([0, 0]))

# Function to draw the letter 'E'
def draw_e(scale_factor):
    side_length = 1.0  # Side length of the E's back
    forward_motion_duration = side_length / forward_velocity
    motions = [
        [forward_velocity, 0, forward_motion_duration],  # Move up the back of 'E'
        [0, -quarter_turn, 0.5],  # Rotate to draw the top bar
        [forward_velocity, 0, forward_motion_duration * 0.5],  # Draw top bar
        [0, half_turn, 0.5],  # Rotate to return
        [forward_velocity, 0, forward_motion_duration * 0.5],  # Return to start of middle bar
        [0, -quarter_turn, 0.5],  # Rotate to draw middle bar
        [forward_velocity, 0, forward_motion_duration * 0.5],  # Draw middle bar
        [0, -quarter_turn, 0.5],  # Rotate to draw bottom bar
        [forward_velocity, 0, forward_motion_duration * 0.5],  # Draw bottom bar
        [0, 0, 1]  # Stop motion
    ]
    execute_motions(motions, np.array([0, 0]), np.array([0, 0]))

# Function to draw the letter 'T'
def draw_t(scale_factor):
    side_length = 1.0  # Side length of the T's top
    forward_motion_duration = side_length / forward_velocity
    motions = [
        [0, -quarter_turn, 0.5],  # Rotate to start top bar
        [forward_velocity, 0, forward_motion_duration],  # Move to draw top of 'T'
        [0, half_turn, 0.5],  # Rotate to draw other half
        [forward_velocity, 0, forward_motion_duration],  # Complete the top bar
        [0, half_turn, 0.5],  # Rotate to go down the middle
        [forward_velocity, 0, forward_motion_duration * 0.5],  # Go down the middle
        [0, 0, 1]  # Stop motion
    ]
    execute_motions(motions, np.array([0, 0]), np.array([0, 0]))
