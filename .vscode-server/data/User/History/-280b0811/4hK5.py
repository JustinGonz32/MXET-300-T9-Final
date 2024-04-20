#!/usr/bin/python3

# L3 program for receiving pre-defined image selection from Node-RED
# Requires the Node-RED flow to send pre-defined image selections to this script
# Communicates with Node-RED using sockets and handles that process using threads

import socket
import json
from threading import Thread
from time import sleep

# UDP communication parameters
IP = "127.0.0.1"                                                        
listen_port = 3553

# Thread function to receive and process image selections from Node-RED
def _imageSelectionUpdater():
    # Socket setup
    dashBoardDatasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dashBoardDatasock.bind((IP, listen_port))
    dashBoardDatasock.settimeout(.25)

    try:
        while True:
            try:
                image_data, recv_addr = dashBoardDatasock.recvfrom(1024)   # Wait and listen for a message from Node-RED
                selected_image = image_data.decode('utf-8')
                if selected_image:
                    # Process the selected image (you can add code here to perform actions based on the selected image)
                    print("Selected image:", selected_image)
                else:
                    print("No image selection received from Node-RED")
            except socket.timeout:
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
