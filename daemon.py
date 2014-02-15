import mosquitto
import config

def on_connect(mosq, obj, rc):
	mosq.subscribe(config.topic, 0)
	# print("rc: "+str(rc))

def on_message(mosq, obj, msg):
	# print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
	f = open("current_status","w")
	f.write(msg.payload)
	f.close()

def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

mqttc = mosquitto.Mosquitto("mumalab_status_daemon_test")
mqttc.username_pw_set(config.broker["user"], config.broker["password"])
mqttc.on_message = on_message
mqttc.on_connect = on_connect
# mqttc.on_subscribe = on_subscribe
mqttc.connect(config.broker["hostname"], config.broker["port"], 60)

mqttc.loop_forever()
