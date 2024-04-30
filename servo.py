from gpiozero import Servo
from time import sleep

# Setup servo on GPIO27 (pin 13), change according to your servo connection
servo = Servo(27)

def set_angle(angle):
    # Convert degrees to servo position and clamp to servo range
    position = angle / 90.0
    servo.value = max(min(position, 1), -1)  # Limit position to range [-1, 1]
    sleep(1)

def servoInt():
    servo.value = None
    print("Detached servo :(")

def main():
    servo.value = None
    try:
        while True:
            user_input = input("Enter angle (-90 to 90) or 'detach' to relax servo: ")
            if user_input.lower() == 'detach':
                servo.value = None  # Detach servo to reduce jitter when not actively controlling
                print("Servo detached.")
            else:
                angle = float(user_input)
                set_angle(angle)
                sleep(1)  # Give time for the servo to move
                servo.value = None
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        servo.value = None  # Detach servo on program exit

if __name__ == "__main__":
    main()
