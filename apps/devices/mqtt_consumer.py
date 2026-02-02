import os
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv('MQTT_HOST', 'mqtt')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))

def on_connect(client, userdata, flags, rc):
    client.subscribe('devices/+/telemetry')

def on_message(client, userdata, msg):
    # Placeholder: parse and persist telemetry
    print('MQTT', msg.topic, msg.payload)

def run_consumer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()
