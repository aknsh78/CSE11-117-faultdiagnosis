import paho.mqtt.client as mqtt
import json
import time
import os

from dotenv import load_dotenv
from sensor_simulator import generate_sensor_data

load_dotenv()

BROKER = "a932b4866647456da95d3f085cde84fb.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = os.getenv("HIVEMQ_USERNAME")
PASSWORD = os.getenv("HIVEMQ_PASSWORD")

TOPIC = "factory/machine1/sensors"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ Cloud")
    else:
        print("Connection failed. Error code:", rc)


client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()

client.on_connect = on_connect

print("Connecting to HiveMQ Cloud...")

client.connect(BROKER, PORT, 60)

# Start MQTT network loop
client.loop_start()

time.sleep(2)

while True:

    data = generate_sensor_data()

    message = json.dumps(data)

    result = client.publish(TOPIC, message)

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("\nPublished:")
        print(message)
    else:
        print("Publish failed. Error:", result.rc)

    time.sleep(0.2)