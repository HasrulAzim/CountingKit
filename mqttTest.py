import time
import sys
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

SENSOR1_COUNTER = 0
SENSOR2_COUNTER = 0

SENSOR1_GPIO = 5
SENSOR2_GPIO = 6

def sensor1_detect_callback(channel):
    global SENSOR1_COUNTER
    if not GPIO.input(SENSOR1_GPIO):
        SENSOR1_COUNTER += 1
        print("Button 1 pressed")
    else:
        print("Button 1 released")
        
def sensor2_detect_callback(channel):
    global SENSOR2_COUNTER
    if not GPIO.input(SENSOR2_GPIO):
        SENSOR2_COUNTER += 1
        print("Button 2 pressed")
    else:
        print("Button 2 released")
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CK.AllID")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR1_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SENSOR2_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(SENSOR1_GPIO, GPIO.FALLING, callback=sensor1_detect_callback, bouncetime=200)
GPIO.add_event_detect(SENSOR2_GPIO, GPIO.FALLING, callback=sensor2_detect_callback, bouncetime=200)

mqttConnected = False

mqttBroker = '100.100.100.110'
mqttPort = 1883
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

while True:
    if mqttConnected == False:
        try:
            client.connect(mqttBroker, mqttPort, 60)    
        except Exception as e:
            print(e, file=sys.stderr)
        else:
            client.loop_start()
            mqttConnected = True
    else:
#         client.publish("CK.Pass", str(SENSOR1_COUNTER))
#         print(GPIO.input(SENSOR1_GPIO))
        print(SENSOR1_COUNTER)
#         client.publish("CK.Reject", str(SENSOR2_COUNTER))
#         print(GPIO.input(SENSOR2_GPIO))
        print(SENSOR2_COUNTER)
#         print(" ")
        time.sleep(2)
