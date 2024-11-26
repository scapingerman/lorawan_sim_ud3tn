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
    
  -  To integrate MQTT data into a DTN architecture, use the mqtt_to_ud3tn.py script. This script captures MQTT messages from ChirpStack, converts them into DTN bundles, and forwards them to a remote uD3TN node. At the destination, these bundles can be extracted and retransmitted as MQTT messages.

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

MQTT Broker: Serves as a bridge between LoRaWAN and DTN architectures by converting MQTT messages into DTN bundles, ensuring reliable data delivery in delay-tolerant networks.


### Next Step
 **Scale the setup:**
 -  Use physical gateways and end devices (e.g., RAK2287, Heltec LoRa V3).

# Integrating the MQTT-to-uD3TN Workflow into a Direct-to-Satellite IoT (DtS-IoT) Scenario

Building upon the strengths of LoRaWAN architectures and DTN protocols, the following outlines how MQTT-to-uD3TN integration aligns with a DtS-IoT scenario:

---

## **Integration of MQTT to uD3TN in DtS-IoT**

### **Background**
The study highlights a LoRaWAN-based DtS-IoT architecture where devices transmit data to satellites. LoRaWAN consists of multiple layers:
- **Network Server:** Handles authentication and routing.
- **Application Server:** Manages data processing and presentation.

A key challenge is efficiently managing intermittent connections between satellites and ground stations while ensuring reliable data transmission.

---

### **Proposed Integration**
Using the MQTT-to-uD3TN workflow, this integration bridges LoRaWAN and DTN capabilities for robust data delivery.

#### **1. Data Capture at the Application Server**
- MQTT data is captured at the **Application Server**, which serves as the intermediary between the LoRaWAN network and external systems.
- Example: Capturing data from a ChirpStack server topic.

#### **2. Transformation into DTN Bundles**
- Captured MQTT data is processed using uD3TN tools (e.g., `aap2_send.py`), transforming it into DTN bundles.  
- These bundles ensure resilience to delays and disruptions, critical for DtS-IoT.

#### **3. Transmission over DTN**
- Bundles are forwarded to a destination node, such as:
  - Another uD3TN instance on a satellite.
  - A ground station node.
- This ensures reliable delivery, even with intermittent connectivity.

---

### **Diagram**

[End Device] -> [Gateway] -> [Network Server] -> [Application Server] -> [MQTT Capture] -> [MQTT Capture] -> [Transformation to DTN Bundles] 



