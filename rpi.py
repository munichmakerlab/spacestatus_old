#/bin/python
import RPi.GPIO as GPIO
import mosquitto

room_open = False

def print_status():
	if room_open:
		print "Current status: open."
		mqtt_client.publish(config.topic, "1", 1, True)
	else:
		print "Current status: closed."
		mqtt_client.publish(config.topic, "0", 1, True)

def status_callback(channel):
	global room_open
	if channel == 23:
		room_open = True
	elif channel == 24:
		room_open = False
	print_status()

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

mqtt_client = mosquitto.Mosquitto("mumalab_status_box")
mqtt_client.username_pw_set(config.broker["user"], config.broker["password"])
mqtt_client.will_set(config.topic, "?", 1, True)
mqtt_client.connect(config.broker["hostname"], config.broker["port"], 60)


GPIO.add_event_detect(23, GPIO.RISING, callback=status_callback, bouncetime=300)
GPIO.add_event_detect(24, GPIO.RISING, callback=status_callback, bouncetime=300)

try:
	while 1:
		mqtt_client.loop()
except KeyboardInterrupt:
	pass

GPIO.cleanup()

