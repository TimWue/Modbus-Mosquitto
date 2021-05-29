import paho.mqtt.client as mqtt
import time
from pymodbus.client.sync import ModbusTcpClient
import json
import logging

# CONFIGS
# MODBUS
MODBUS_IP = '192.168.178.250'
MODBUS_PORT = 502
SENSOR_NAMES = ['sensor1', 'sensor2', 'sensor3']
MODBUS_REGISTER_ADDRESSES = [1000, 2000, 3000]

# MQTT
CONNECT_MQTT = True
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

mbclient = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)
mbclient.connect()
while True:
    for i in range(3):
        rectemp = -999
        try:
            rec = None
            #logging.info("Connected to " + MODBUS_IP + " on Port " + MODBUS_PORT)
            rec = mbclient.read_input_registers(MODBUS_REGISTER_ADDRESSES[i], 3)
            if rec:
                rectemp = rec.registers[2] / 40
                logging.info('Received ' + str(rectemp))
        except:
            #mbclient.close()
            logging.warning('Failed to Connect to Modbus')
            time.sleep(2)

        data = {"sensorName": SENSOR_NAMES[i], "time": time.time(), "value": rectemp}
        tempdata = json.dumps(data)
        if CONNECT_MQTT:
            client.publish("tempSensor", tempdata)
            logging.info("Published " + str(rectemp) + " °C, from Sensor: " + SENSOR_NAMES[i])
    time.sleep(0.5)
