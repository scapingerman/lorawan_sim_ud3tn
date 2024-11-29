import subprocess
import paho.mqtt.client as mqtt
import json

# MQTT configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "application/18735dd4-3b5f-47d2-a0f5-a0c5f48d80a4/device/8e2f811d9394fe0d/event/up"

# Function to process MQTT messages and send them to uD3TN
def on_message(message):
    payload = message.payload.decode("utf-8")  
    
    command = [
        "python3", 
        "/home/grmn/.local/lib/python3.8/site-packages/ud3tn_utils/aap2/bin/aap2_send.py",  # Replace with the correct path!
        "--tcp", 
        "localhost", 
        "4242",  # Port of the uD3TN node
        "dtn://b.dtn/bundlesink",  # Destination EID
        payload  # Message
    ]

    # Send the bundle
    subprocess.run(command, check=True)
    print('MQTT SENT TO µD3TN')

# MQTT configuration
client = mqtt.Client()

# Connect to the broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Set up the callback function to receive messages
client.on_message = on_message
# Subscribe to the MQTT topic
client.subscribe(MQTT_TOPIC)
# Keep the client running
client.loop_forever()
