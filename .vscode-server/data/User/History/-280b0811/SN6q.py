#!/usr/bin/python3

# L3 program for receiving pre-defined image selection from Node-RED
# Requires the Node-RED flow to send pre-defined image selections to this script
# Communicates with Node-RED using sockets and handles that process using threads

import socket
import json
from threading import Thread

# UDP communication parameters
IP = "127.0.0.1"                                                        
listen_port = 3553

# Thread function to receive and process image selections from Node-RED
def image_selection_updater():
    # Socket setup
    dash_board_data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dash_board_data_sock.bind((IP, listen_port))
    dash_board_data_sock.settimeout(0.25)

    try:
        while True:
            try:
                image_data, recv_addr = dash_board_data_sock.recvfrom(1024)   # Wait and listen for a message from Node-RED
                if not image_data:
                    continue  # Skip empty data
                image_data = json.loads(image_data)                          # Load the JSON message to a Python dictionary
                
                # Extract the selected image from the received data
                selected_image = image_data.get('selected_image', None)
                
                if selected_image is not None:
                    # Process the selected image (you can add code here to perform actions based on the selected image)
                    print("Selected image:", selected_image)
                else:
                    print("No image selection received from Node-RED")
            except socket.timeout:                                          # Timeout occurs if the listener waits too long
                print("Socket timeout occurred")
            except json.JSONDecodeError as e:
                print("JSON decoding error:", e)
    except Exception as ex:
        print("Error:", repr(ex))
    finally:
        dash_board_data_sock.close()  # Close the socket when done

# Run only when this script is directly executed
if __name__ == "__main__":
    # Create and start the imageSelectionThread
    image_selection_thread = Thread(target=image_selection_updater)
    image_selection_thread.daemon = True
    image_selection_thread.start()

    try:
        while True:
            pass  # Keep the main thread running
    except KeyboardInterrupt:
        print("Script terminated")
