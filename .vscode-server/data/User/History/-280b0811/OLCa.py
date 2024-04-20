import socket
import json
from threading import Thread

# UDP communication parameters
IP = "127.0.0.1"                                                        
listen_port = 3553

# Socket setup
dashBoardDatasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dashBoardDatasock.bind((IP, listen_port))
dashBoardDatasock.settimeout(5)  # Increased timeout to 5 seconds

# Thread function to receive and process image selections from Node-RED
def _imageSelectionUpdater():
    while True:
        try:
            image_data, recv_addr = dashBoardDatasock.recvfrom(1024)   # Wait and listen for a message from Node-RED
            
            if not image_data:
                print("No data received")
                continue
            
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
        except json.JSONDecodeError:
            print("Error decoding JSON data")
        except Exception as ex:
            print("Error:", repr(ex))

def main():
    while True:
        pass  # Keep the main thread running

if __name__ == "__main__":
    # Create the imageSelectionThread
    imageSelectionThread = Thread(target=_imageSelectionUpdater)
    imageSelectionThread.daemon = True
    
    # Start the imageSelectionThread
    imageSelectionThread.start()

    try:
        main()
    except KeyboardInterrupt:
        print("Script terminated")
