#/bin/python
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
from threading import Timer
import logging

import config

room_open = False

def on_connect(mosq, obj, rc):
	logging.info("Connect with RC " + str(rc))
	# Get initial status
	set_status(23)

def on_disconnect(client, userdata, rc):
	logging.warning("Disconnected (RC " + str(rc) + ")")
	if rc <> 0:
		try_reconnect(client)

def on_log(client, userdata, level, buf):
	logging.debug(buf)

# MQTT reconnect
def try_reconnect(client, time = 60):
	try:
		logging.info("Trying reconnect")
		client.reconnect()
	except:
		logging.warning("Reconnect failed. Trying again in " + str(time) + " seconds")
		Timer(time, try_reconnect, [client]).start()

# post the status to MQTT and the local console
def print_status():
	logging.info("Publishing status to MQTT")
	if room_open:
		logging.info("Current space status: open")
		mqttc.publish(config.topic, "1", 1, True)
	else:
		logging.info("Current space status: closed")
		mqttc.publish(config.topic, "0", 1, True)

# after timer has fired, get the status
def set_status(channel):
	global room_open
	logging.info("Getting status from GPIO")
	if GPIO.input(channel) == GPIO.HIGH:
		room_open = True
	else:
		room_open = False
	logging.info("Current Status: " + str(room_open))
	print_status()

# Reset timer when interrupt is received
def status_callback(channel):
	global bounce_timer
	logging.info("GPIO interrupt detected")
	bounce_timer.cancel()
	bounce_timer = Timer(2.0, set_status, [channel])
	bounce_timer.start()

logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

# create timer initialy so it can be canceled
bounce_timer = Timer(5.0, set_status)

# initialize GPIO
logging.info("Initializing GPIO")
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# initialize MQTT
logging.info("Initializing MQTT")
mqttc = paho.Client("mumalab_status_box")
mqttc.username_pw_set(config.broker["user"], config.broker["password"])
mqttc.will_set(config.topic, "?", 1, True)
mqttc.connect(config.broker["hostname"], config.broker["port"], 60)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_log = on_log

# add interrupt to GPIO pin
logging.info("Adding interrupt")
GPIO.add_event_detect(23, GPIO.BOTH, callback=status_callback)

# Loop forever
logging.info("Entering loop")
mqttc.loop_forever()

# Clean up afterwards
logging.info("Cleanup")
GPIO.cleanup()
mqttc.disconnect()
