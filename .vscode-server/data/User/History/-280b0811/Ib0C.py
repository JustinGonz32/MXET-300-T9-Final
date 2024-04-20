def main():
    # Start the image selection thread
    imageSelectionThread.start()
    
    while True:
        try:
            # Receive data from Node-RED
            image_data, recv_addr = dashBoardDatasock.recvfrom(1024)
            image_data = json.loads(image_data)
            
            # Extract the selected image from the received data
            selected_image = image_data.get('selected_image', None)
            
            if selected_image is not None:
                # Process the selected image (you can add code here to perform actions based on the selected image)
                print("Selected image:", selected_image)
            else:
                print("No image selection received from Node-RED")
                
        except socket.timeout:
            print("Socket timeout occurred")
        except Exception as ex:
            print("Error:", repr(ex))

if __name__ == "__main__":
    main()
