import paho.mqtt.client as paho
from threading import Timer
import logging

import config

def on_connect(mosq, obj, rc):
	logging.info("Connect with RC " + str(rc))
	mosq.subscribe(config.topic, 0)

def on_message(mosq, obj, msg):
	logging.info(msg.topic + " [" + str(msg.qos) + "]: " + str(msg.payload))
	if msg.payload == "1":
		mqttc.publish("mumalab/room/lights/whiteboard/state", "1", 1, False)
		mqttc.publish("mumalab/room/lights/hanging_lights/state", "1", 1, False)
		mqttc.publish("mumalab/room/lights/chandelier/state", "1", 1, False)
	elif msg.payload == "0":
		mqttc.publish("mumalab/room/lights/whiteboard/state", "0", 1, False)
		mqttc.publish("mumalab/room/lights/hanging_lights/state", "0", 1, False)
		mqttc.publish("mumalab/room/lights/chandelier/state", "0", 1, False)
	

def on_subscribe(mosq, obj, mid, granted_qos):
	logging.info("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_disconnect(client, userdata, rc):
	logging.warning("Disconnected (RC " + str(rc) + ")")
	if rc <> 0:
		try_reconnect(client)

def on_log(client, userdata, level, buf):
	logging.debug(buf)
	
def try_reconnect(client, time = 60):
	try:
		logging.info("Trying reconnect")
		client.reconnect()
	except:
		logging.warning("Reconnect failed. Trying again in " + str(time) + " seconds")
		Timer(time, try_reconnect, [client]).start()

logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

logging.info("Initializing MQTT")
mqttc = paho.Client()
mqttc.username_pw_set(config.broker["user"], config.broker["password"])
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
try:
	mqttc.connect(config.broker["hostname"], config.broker["port"])
except:
	logging.warning("Connection failed. Trying again in 30 seconds")
	Timer(30, try_reconnect, [mqttc]).start()

logging.info("Entering loop")
try:
	mqttc.loop_forever()
except KeyboardInterrupt:
	pass

logging.info("Exiting")
mqttc.disconnect()
