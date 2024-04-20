#!/usr/bin/python3

# L3 program for receiving pre-defined image selection from Node-RED
# Requires the Node-RED flow to send pre-defined image selections to this script
# Communicates with Node-RED using sockets and handles that process using threads
#!/usr/bin/python3
import socket
import json
from threading import Thread
from time import sleep

# UDP communication parameters
IP = "127.0.0.1"                                                        
listen_port = 3553

# Socket setup
dashBoardDatasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dashBoardDatasock.bind((IP, listen_port))
dashBoardDatasock.settimeout(.25)

# Global variable to store the selected shape
selected_shape = None

# Function to receive and process image selections from Node-RED
def _shapeSelectionUpdater():
    global selected_shape
    while True:
        try:
            image_data, recv_addr = dashBoardDatasock.recvfrom(1024)   # Wait and listen for a message
            selected_shape = image_data.decode('utf-8').strip()        # Decode the received byte string to get the selected shape
        except socket.timeout:                                         # Timeout occurs if the listener waits too long
            pass
        except Exception as ex:
            print("Error:", repr(ex))

# Configure the thread
shapeSelectionThread = Thread(target=_shapeSelectionUpdater)
shapeSelectionThread.daemon = True
shapeSelectionThread.start()

# Function to use the selected shape
def use_selected_shape():
    global selected_shape
    while True:
        if selected_shape is not None:
            print("Selected shape:", selected_shape)
            # Perform actions based on the selected shape here
            # For example, call the corresponding function from shapeMotions.py
            # You can pass the selected shape as an argument to the function
            # shapeMotions.draw_shape(selected_shape)
            selected_shape = None  # Reset the selected shape after using it
        sleep(0.5)  # Adjust the sleep time as needed

# Run only when this script is directly executed
if __name__ == "__main__":
    try:
        while True:
            use_selected_shape()
            
# Thread function to receive and process image selections from Node-RED
def _imageSelectionUpdater():
    try:
        while True:
            image_data, recv_addr = dashBoardDatasock.recvfrom(1024)   # Wait and listen for a message from Node-RED
            image_data = json.loads(image_data)                        # Load the JSON message to a Python dictionary
            
            # Extract the selected image from the received data
            selected_image = image_data.get('selected_image', None)
            
            if selected_image is not None:
                # Process the selected image (you can add code here to perform actions based on the selected image)
                print("Selected image:", selected_image)
            else:
                print("No image selection received from Node-RED")
                
    except socket.timeout:                                          # Timeout occurs if the listener waits too long
        print("Socket timeout occurred")
    except Exception as ex:
        print("Error:", repr(ex))
    finally:
        dashBoardDatasock.close()  # Close the socket when done

# Run only when this script is directly executed
if __name__ == "__main__":
    # Create and start the imageSelectionThread
    imageSelectionThread = Thread(target=_imageSelectionUpdater)
    imageSelectionThread.daemon = True
    imageSelectionThread.start()

    try:
        while True:
            pass  # Keep the main thread running
    except KeyboardInterrupt:
        print("Script terminated")
