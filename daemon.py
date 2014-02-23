import paho.mqtt.client as paho
from threading import Timer

import config

def on_connect(mosq, obj, rc):
	print "[MQTT] Connect with RC " + str(rc)
	mosq.subscribe(config.topic, 0)
	# print("rc: "+str(rc))

def on_message(mosq, obj, msg):
	print "[MQTT] " + msg.topic + " [" + str(msg.qos) + "]: " + str(msg.payload)
	f = open("current_status","w")
	f.write(msg.payload)
	f.close()

def on_subscribe(mosq, obj, mid, granted_qos):
	print "[MQTT] Subscribed: "+str(mid)+" "+str(granted_qos)

def on_disconnect(client, userdata, rc):
	print "[MQTT] Disconnected " + str(rc)
	try_reconnect(client)

def on_log(client, userdata, level, buf):
	print "[MQTT] LOG: " + buf
	
def try_reconnect(client, time = 60):
	try:
		print "[MQTT] Trying reconnect"
		client.reconnect()
	except:
		print "[MQTT] Reconnect failed. Trying again in " + str(time) + " seconds"
		Timer(time, try_reconnect, [client]).start()


print "[Main] Initializing MQTT"
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
	print "[MQTT] Connection failed. Trying again in 30 seconds"
	Timer(30, try_reconnect, [mqttc]).start()

print "[Main] Entering loop"
mqttc.loop_forever()

print "[Main] Exiting"
mqttc.disconnect()
