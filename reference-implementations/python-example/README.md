# Python reference project for firstmile-proto

The demo project consists of two scripts: 
* `data-sender.py` simulates a Data Sender, a device such as a datalogger that transmits measurement data from the remote AWS.
* `data-receiver.py` starts a listener that subscribes to a MQTT broker, receives messages published by Data Sender, differentiates them by topic (site), and displays the metadata and received values on graphs. 
* `payload-generator.py` reads the schema bindings from JSON file, and generates sample Metadata and Data messages (in JSON format for readbility)

## Install

    $ pipenv install
    $ apt-get update && apt install -y protobuf-compiler

## Generate protobuf code

    $ pipenv run build-proto

## Start receiver

    $ python3 data-receiver.py --broker s87beff9.ala.eu-central-1.emqxsl.com --port 8883 --tls --insecure --topic "firstmile/#"  --username geolux --password "XXXX"

Replace the broker address, port, topic, username and password with your data.

After starting the receiver, open browser and go to the following URL: http://localhost:8050

## Start sender

Example to run the sender to send both measurement and metadata, for site 1:
    
    $ python3 data-sender.py --period 10 --vendor geolux --hostid "AWS123" --broker s87beff9.ala.eu-central-1.emqxsl.com --username geolux --password "XXXX" --port 8883 --tls --insecure

## Run payload generator to create example messages

    $ python3 payload-generator.py

The created JSON files with payloads will be stored to /standard/examples/example_output