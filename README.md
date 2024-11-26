# lorawan_sim_ud3tn

# LoRaWAN-DTN Integration with LWN Simulator, ChirpStack, and uD3TN

This repository provides a comprehensive guide to simulate a LoRaWAN environment using **LWN Simulator**, manage data with **ChirpStack**, and forward bundles to **uD3TN**. This architecture is suitable for IoT applications in environments with intermittent connectivity.

---

## Requirements

1. **Docker** (for ChirpStack deployment).
2. **Python 3.x** with required libraries (e.g., `paho-mqtt`).
3. Access to [LWN Simulator](https://github.com/UniCT-ARSLab/LWN-Simulator).
4. Custom scripts for integrating MQTT with uD3TN.

---

## Usage Instructions

### 1. Setup and Run LWN Simulator

LWN Simulator creates a virtual LoRaWAN environment with devices, forwarders, and gateways.

1. **Installation**:
   - Clone the repository:
     ```bash
     git clone https://github.com/UniCT-ARSLab/LWN-Simulator.git
     cd LWN-Simulator
     ```
   - Follow installation steps in the [LWN Simulator README](https://github.com/UniCT-ARSLab/LWN-Simulator#installation).

2. **Run the simulator**:
   - Navigate to the simulator directory and execute:
     ```bash
     cd lwnsimulator_x64
     ./lwnsimulator_x64
     ```
   - Use the web interface to add gateways and end devices.

3. **Features**:
   - Supports LoRaWAN v1.0.3 specification.
   - Allows customization of payloads, MAC commands, and device classes (A, B, C).

---

### 2. Deploy ChirpStack Using Docker

ChirpStack is an open-source LoRaWAN Network Server stack.

1. **Clone the ChirpStack Docker repository**:
   ```bash
   git clone https://github.com/chirpstack/chirpstack-docker.git
   cd chirpstack-docker
   ```
   

2. **Start the Docker containers:**

   ```bash
    sudo docker-compose up
   ```

3. **Configuration:**

  -  Edit configuration/chirpstack/chirpstack.toml to adjust the regional settings if needed.
  -  Use the provided docker-compose.yml as a base and modify it for production as necessary.

4. **Components:**
   -  ChirpStack Gateway Bridge: Connects gateways to the Network Server.
   -  ChirpStack Network Server: Processes and routes LoRaWAN packets.
   -  ChirpStack Application Server: Publishes received data to an MQTT topic.


### 3. Capture MQTT Data and Send to uD3TN
    
  -  To capture MQTT data from ChirpStack and forward it to a uD3TN node as DTN bundles, use the mqtt_to_ud3tn.py script. This script subscribes to a specific MQTT topic, processes incoming messages, and forwards them to uD3TN. Run it as follows:

  ```bash
  python3 mqtt_to_ud3tn.py
  ```
1. **How It Works:**:
    - MQTT Topic: The MQTT_TOPIC variable in the script corresponds to the topic where ChirpStack publishes data.
For example:

 ```bash

application/400d3f3b-c7ea-4d4d-8ac5-f7f1b4bcc34e/device/8e2f811d9394fe0d/event/up

 ```
  -  400d3f3b-c7ea-4d4d-8ac5-f7f1b4bcc34e
This is the Application ID assigned when configuring the application in ChirpStack.

  -  8e2f811d9394fe0d

This is the End Device ID, representing the specific LoRaWAN device transmitting data.

  -  Data Flow: The script captures messages from the MQTT broker, extracts the payload, and sends it to a uD3TN node using the aap2_send.py tool.

2. **MQTT Data Capture in the LoRaWAN Architecture:**
Below is a diagram illustrating where the MQTT data is captured in the typical LoRaWAN architecture:

 ```bash
End Device --> Gateway --> Network Server --> Application Server --> [MQTT Broker] --> uD3TN
 ```

End Device: Sends LoRa frames to the Gateway.

Gateway: Forwards frames to the Network Server.

Network Server: Processes frames, applies network rules, and forwards the data to the Application Server.

Application Server: Publishes processed data to the MQTT Broker.

MQTT Broker: Hosts topics where applications, like your script, can subscribe and retrieve messages for further processing.
This script bridges the LoRaWAN and DTN architectures by transforming MQTT messages into DTN bundles


### Next Step
 **Scale the setup:**
 -  Use physical gateways and end devices (e.g., RAK2287, Heltec LoRa V3).

