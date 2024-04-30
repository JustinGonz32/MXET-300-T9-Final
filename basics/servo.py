import RPi.GPIO as GPIO
from time import sleep

# Set the GPIO numbering mode to BOARD
GPIO.setmode(GPIO.BOARD)
# Set pin 13 as an output pin
GPIO.setup(13, GPIO.OUT)

# Initialize PWM on pin 13 with a frequency of 50Hz
pwm = GPIO.PWM(13, 50)
pwm.start(0)

def SetAngle(angle):
    """
    This function sets the angle of the servo motor.
    Args:
        angle (int): The angle to which the servo motor should rotate.
    """
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    pwm.ChangeDutyCycle(0)  # Stop sending a signal to the servo

def main():
    try:
        while True:
            usAngle = int(input("Enter Angle: "))
            SetAngle(usAngle)
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        pwm.stop()  # Stop the PWM output
        GPIO.cleanup()  # Clean up GPIO to ensure all channels are reset

if __name__ == "__main__":
    main()
