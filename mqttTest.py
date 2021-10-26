import time
import sys
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

SENSOR1_GPIO = 5
SENSOR2_GPIO = 6

SENSOR1_COUNTER = 0
SENSOR2_COUNTER = 0

mqttBroker = '100.100.100.110'
mqttPort = 1883

def sensor1_detect_callback(channel):
    SENSOR1_COUNTER += 1

    
def sensor2_detect_callback(channel):
    SENSOR2_COUNTER += 1

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

GPIO.add_event_detect(SENSOR1_GPIO, GPIO.RISING, callback=sensor1_detect_callback, bouncetime=100)
GPIO.add_event_detect(SENSOR2_GPIO, GPIO.RISING, callback=sensor2_detect_callback, bouncetime=100)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqttBroker, mqttPort, 60)
client.loop_start()

while True:
    client.publish("CK.Pass", SENSOR1_COUNTER)
