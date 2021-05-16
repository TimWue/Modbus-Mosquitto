import paho.mqtt.client as mqtt
import time
from pymodbus.client.sync import ModbusTcpClient
import json
import logging

# CONFIGS
# MODBUS
MODBUS_IP = "192.168.178.250"
MODBUS_PORT = 1000
SENSOR_NAMES = ['sensor1', 'sensor2', 'sensor3']
MODBUS_REGISTER_ADDRESSES = [1000, 2000, 3000]

# MQTT
CONNECT_MQTT = False
MQTT_CLIENT_NAME = "ModbusClient"
MQTT_BROKER_NAME = "mosquitto-broker"

# LOGGING
SAVE_TO_FILE = False
LOG_LEVEL = logging.INFO
LOG_FILE_NAME = "modbus.log"

# PROGRAM
if SAVE_TO_FILE:
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG)
else:
    logging.basicConfig(level=LOG_LEVEL)

if CONNECT_MQTT:
    client = mqtt.Client(MQTT_CLIENT_NAME)
    client.connect(MQTT_BROKER_NAME)

while True:
    for i in range(3):
        rectemp = -999
        try:
            mbclient = ModbusTcpClient(MODBUS_IP, MODBUS_PORT)
            logging.info("Connected to " + MODBUS_IP + " on Por " + MODBUS_PORT)
            rec = mbclient.read_input_registers(MODBUS_REGISTER_ADDRESSES[i], 3)
            if rec:
                rectemp = rec[2] / 40
                logging.info('Received' + str(rectemp))
        except:
            logging.warning('Failed to Connect to Modbus')

        data = {"sensorName": SENSOR_NAMES[i], "time": time.time(), "value": rectemp}
        tempdata = json.dumps(data)
        logging.info("Published " + str(rectemp) + " °C, from Sensor: " + SENSOR_NAMES[i])
        if CONNECT_MQTT:
            client.publish("tempSensor", tempdata)
    time.sleep(0.5)
