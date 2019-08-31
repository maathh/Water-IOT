import paho.mqtt.publish as publish

MQTT_SERVER = "172.16.71.53"
MQTT_PATH = "teste"

publish.single(MQTT_PATH, "PIPIPIPOPOPO", hostname=MQTT_SERVER)