import sys
import RPi.GPIO as GPIO

SENSOR1_GPIO = 5
SENSOR2_GPIO = 6

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def sensor1_detect_callback(channel):
    if GPIO.input(SENSOR1_GPIO) == False:    
        print("Sensor 1 pressed!")
    
def sensor2_detect_callback(channel):
    print("Sensor 2 pressed!")
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR1_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SENSOR2_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(SENSOR1_GPIO, GPIO.RISING, callback=sensor1_detect_callback, bouncetime=100)
    GPIO.add_event_detect(SENSOR2_GPIO, GPIO.RISING, callback=sensor2_detect_callback, bouncetime=100)
