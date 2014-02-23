#/bin/python
import RPi.GPIO as GPIO
import paho.mqtt.client as paho

from threading import Timer

room_open = False

def on_disconnect(client, userdata, rc):
	print "[MQTT] Disconnected " + str(rc)
	try_reconnect(client)

def on_log(client, userdata, level, buf):
	print "[MQTT] LOG: " + buf

# MQTT reconnect
def try_reconnect(client, time = 60):
	try:
		print "[MQTT] Trying reconnect"
		client.reconnect()
	except:
		print "[MQTT] Reconnect failed. Trying again in " + str(time) + " seconds"
		Timer(time, try_reconnect, [client]).start()


# post the status to MQTT and the local console
def print_status():
	print "[MQTT] Publishing status"
	if room_open:
		mqttc.publish(config.topic, "1", 1, True)
	else:
		print "Current status: closed."
		mqttc.publish(config.topic, "0", 1, True)

# after timer has fired, get the status
def set_status(channel):
	global room_open
	print "[GPIO] Getting status"
	if GPIO.input(channel) == GPIO.HIGH:
		room_open = True
	else:
		room_open = False
	print "[GPIO] Current Status: " + str(room_open)
	print_status()

# Reset timer when interrupt is received
def status_callback(channel):
	global bounce_timer
	print "[GPIO] interrupt detected"
	bounce_timer.cancel()
	bounce_timer = Timer(2.0, set_status, [channel])
	bounce_timer.start()

# create timer initialy so it can be canceled
bounce_timer = Timer(5.0, set_status)

# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# initialize MQTT
mqttc = paho.client("mumalab_status_box")
mqttc.username_pw_set(config.broker["user"], config.broker["password"])
mqttc.will_set(config.topic, "?", 1, True)
mqttc.connect(config.broker["hostname"], config.broker["port"], 60)

# add interrupt to GPIO pin
GPIO.add_event_detect(23, GPIO.BOTH, callback=status_callback)

# Loop forever
mqttc.loop_forever()

# Clean up afterwards
GPIO.cleanup()
mqttc.disconnect()
