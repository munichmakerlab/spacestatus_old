#/bin/python
import RPi.GPIO as GPIO
import mosquitto
from threading import Timer

room_open = False

# post the status to MQTT and the local console
def print_status():
	if room_open:
		print "Current status: open."
		mqtt_client.publish(config.topic, "1", 1, True)
	else:
		print "Current status: closed."
		mqtt_client.publish(config.topic, "0", 1, True)

# after timer has fired, get the status
def set_status(channel):
	global room_open
	if GPIO.input(channel) == GPIO.HIGH:
		room_open = True
	else:
		room_open = False
	print_status()

# Reset timer when interrupt is received
def status_callback(channel):
	global bounce_timer
	bounce_timer.cancel()
	bounce_timer = Timer(2.0, set_status, [channel])
	bounce_timer.start()

# create timer initialy so it can be canceled
bounce_timer = Timer(5.0, set_status)

# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# initialize MQTT
mqtt_client = mosquitto.Mosquitto("mumalab_status_box")
mqtt_client.username_pw_set(config.broker["user"], config.broker["password"])
mqtt_client.will_set(config.topic, "?", 1, True)
mqtt_client.connect(config.broker["hostname"], config.broker["port"], 60)

# add interrupt to GPIO pin
GPIO.add_event_detect(23, GPIO.BOTH, callback=status_callback)

# Loop forever
try:
	while 1:
		mqtt_client.loop()
except KeyboardInterrupt:
	pass

# Clean up afterwards
GPIO.cleanup()
mqtt_client.disconnect()
