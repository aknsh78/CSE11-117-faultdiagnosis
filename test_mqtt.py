import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

BROKER = "a932b4866647456da95d3f085cde84fb.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = os.getenv("HIVEMQ_USERNAME")
PASSWORD = os.getenv("HIVEMQ_PASSWORD")

print("Username:", repr(USERNAME))
print("Password loaded:", bool(PASSWORD))

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()

print("Trying to connect...")

try:
    client.connect(BROKER, PORT, 60)
    print("SUCCESS! Python connected to HiveMQ.")
except Exception as e:
    print("FAILED:", repr(e))