# Simple data sender
# Emulates an AWS then sends periodic temperature measurements using 1M-TT protocol.
# The script will first send a single Metadata message with site configuration info, it will be sent as MQTT retained message.
# Then it will periodically publish Data messages with temperature and voltage readings. 
#
# Before running this script, ensure that proto schema is compiled and the protobuf classes are generated. This can be achieved by running the
# following command in protos folder: 
# protoc -I . --python_out=../python-example/ firstmile.proto 
#
# Example fo running this script:
# python3 data-sender.py --period 10 --vendor geolux --hostid "AWS123" --broker s87beff9.ala.eu-central-1.emqxsl.com --username geolux --password "XXXX" --port 8883 --tls --insecure

import argparse
import random
import time
import ssl
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
import firstmile_pb2 as pb2 # Your generated protobuf classes
from google.protobuf.timestamp_pb2 import Timestamp


# These function just create some fake measurements
def random_temperature():
    return round(random.uniform(-40.0, 40.0), 2)

def random_voltage():
    return round(random.uniform(11.5, 13.0), 2)

def current_timestamp():
    t = Timestamp()
    now = datetime.now(timezone.utc)
    t.FromDatetime(now)
    return t


# The following function will create protobuf objects with the parameter definitions
def define_parameters():
    # Data Logger parameters
    pd1 = pb2.ParameterDefinition()
    pd1.id = 1
    pd1.description = "Internal parameters of the data-logger"

    param_voltage = pb2.Parameter()
    param_voltage.longName = "Supply Voltage"
    param_voltage.unit = "V"
    param_voltage.standardName = "voltage"
    param_voltage.observerId = 1
    param_voltage.cellMethod = pb2.POINT
    param_voltage.cellPeriodSeconds = 0

    param_internal_temp = pb2.Parameter()
    param_internal_temp.longName = "Internal Temperature"
    param_internal_temp.unit = "°C"
    param_internal_temp.standardName = ""
    param_internal_temp.observerId = 1
    param_internal_temp.cellMethod = pb2.MEAN
    param_internal_temp.cellPeriodSeconds = 5

    pd1.parameters.extend([param_voltage, param_internal_temp])

    # PT100 sensor parameters
    pd2 = pb2.ParameterDefinition()
    pd2.id = 2
    pd2.description = "PT100 temperature sensor readings"

    param_air_temp = pb2.Parameter()
    param_air_temp.longName = "Surface Air Temperature"
    param_air_temp.unit = "°C"
    param_air_temp.standardName = "air_temperature"
    param_air_temp.observerId = 2
    param_air_temp.cellMethod = pb2.MEAN
    param_air_temp.cellPeriodSeconds = 30

    pd2.parameters.extend([param_air_temp])

    return [pd1, pd2]

# This function creates a measurement Observation message with simulated values
def generate_observations(parameter_defs):
    observations = []

    # Loop over parameter definitions
    for pd in parameter_defs:
        obs = pb2.Observation()
        obs.parameterDefinitionId = pd.id
        obs.time.CopyFrom(current_timestamp())

        # For each Parameter in this ParameterDefinition
        for param in pd.parameters:
            val = pb2.Value()

            if param.standardName == "voltage":
                val.doubleValue = random_voltage()
            else:
                val.doubleValue = random_temperature()

            obs.values.append(val)

        observations.append(obs)

    return observations

# Create the metadata
def create_metadata():
    # Host device
    host = pb2.HostDevice()
    host.name = "ArcticX100 Data Logger"
    host.location.latitude = -90
    host.location.longitude = 0
    host.location.heightMeter = 10.0
    host.location.referenceSurface = pb2.GL
    host.url = "https://org.com/data/obs_meta.json"
    host.serialNumber = "1234567890"
    host.firmwareVersion = "1.0.0"

    # Observer device (PT100)
    observer = pb2.ObserverDevice()
    observer.id = 1
    observer.name = "PT100"
    observer.location.latitude = -90
    observer.location.longitude = 0
    observer.location.heightMeter = 13.0
    observer.location.referenceSurface = pb2.GL
    observer.url = "https://org.com/data/obs_meta.json"
    observer.serialNumber = "00AB-123456"
    observer.firmwareVersion = "5.6A-Rev2"

    return host, [observer]

# This is the main function to construct Data message
def build_data_transmission(hostid):
    transmission = pb2.Data()
    transmission.version = 1
    transmission.hostId = hostid

    param_defs = define_parameters()
    observations = generate_observations(param_defs)

    transmission.observations.extend(observations)

    return transmission

def build_metadata_transmission():
    metadata = pb2.Metadata()

    # Define the host device and observers
    host, observers = create_metadata()
    metadata.host.CopyFrom(host)
    metadata.observers.extend(observers)

    # Define the parameter definitions
    param_defs = define_parameters()
    metadata.parameterDefinitions.extend(param_defs)

    return metadata

# MQTT(s) data exchange
def send_mqtt_payload(args, topic, payload_bytes, retain=False):
    client = mqtt.Client()

    if args.username and args.password:
        client.username_pw_set(args.username, args.password)

    if args.tls:
        client.tls_set(
            ca_certs=args.ca_cert,
            certfile=args.client_cert,
            keyfile=args.client_key,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        client.tls_insecure_set(args.insecure)

    print(f"Connecting to MQTT broker {args.broker}:{args.port}...")
    client.connect(args.broker, args.port, 60)
    client.publish(topic, payload_bytes, qos = 2 if retain else 1, retain = retain)
    print(f"Published payload ({len(payload_bytes)} bytes) to topic '{topic}'")
    client.disconnect()

# Main
def main():
    parser = argparse.ArgumentParser(description="AWS MQTT Data Sender PoC")
    parser.add_argument("--broker", required=True, help="MQTT broker address")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--vendor", required=True, help="Vendor name")
    parser.add_argument("--hostid", required=True, help="Host ID")
    parser.add_argument("--period", type=int, default=10, help="Period in seconds between measurements")
    parser.add_argument("--username", help="MQTT username (optional)")
    parser.add_argument("--password", help="MQTT password (optional)")
    parser.add_argument("--tls", action="store_true", help="Enable TLS (MQTTS)")
    parser.add_argument("--ca-cert", help="CA certificate file for TLS connection")
    parser.add_argument("--client-cert", help="Client certificate file for mutual TLS (optional)")
    parser.add_argument("--client-key", help="Client private key file for mutual TLS (optional)")
    parser.add_argument("--insecure", action="store_true", help="Skip server certificate verification")


    args = parser.parse_args()

    # build and send metadata transmission
    metadata = build_metadata_transmission()
    payload_bytes = metadata.SerializeToString()
    topic = f"firstmile/{args.vendor}/metadata/{args.hostid}"
    send_mqtt_payload(args, topic, payload_bytes, retain=True)

    while True:
        # build and send data transmission
        data_transmission = build_data_transmission(args.hostid)
        payload_bytes = data_transmission.SerializeToString()
        topic = f"firstmile/{args.vendor}/data/{args.hostid}"
        send_mqtt_payload(args, topic, payload_bytes)

        # wait for the specified period before sending the next measurement
        time.sleep(args.period)

if __name__ == "__main__":
    main()
