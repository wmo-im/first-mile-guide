# First Mile Guide
WMO First Mile Data Collection Guide

This repository contains all related material pertaining to the SC-IMT Task Team First Mile. The terms of reference of the task team are as follow:

* Draft a list of requirements for the protocols and data formats of the first-mile interface standard.
* Assess existing protocols and data formats against the established requirements.
* Draft a guidance document for the standardization of the first-mile interface, addressing both the protocol and the data format aspects.

This repository is a placeholder for :

* The future First Mile Guide to be presented at INFCOM-4 (in the `first-mile-guide` directory)
* The material related to the Proof of Concept work that is running from Septembre 2025 to Novembre 2025

The Proof Of Concept is based on :

* a protobuf data schema
* a MQTT broker that wil be used to exchange the data between the "Data Senders" (a predifined list of HMEI and WMO Members with publication access rights) and "Data Receivers". Many members of the Task Team will work on their own implementation of a Data Receiver software compliant with the agreed solution.

The folder structure is :

* `first-mile-guide` - This folder contains source for Guide document in adoc format
* `reference-implementations` - Example implementations of first mile protocol senders and receivers
* `requirements` - Information on protocol requirements for participants in proof-of-concept testing - this also gives protocol overview so this is a good place to get familiarized with the protocol
* `standard` - Contains the Protobuf schema and payload examples for various scenarios


This is a work in progress folder that everyone interested can have access to.

It has been decided to open the Proof of Concept work to additional parties as "Data Receivers" only. No support will be given to the "Data Receivers" and they can use the available material without guarantee that it will work.

Access to the shared MQTT broker can be made available as `subscribe` only. Username and password can be requested by creating a new issue on the repository explaining the intention of use and providing some details on the requester. Beyond providing the username/password, no further support will be provided. 

The MQTT Topic Hierarchy used during the Proof Of Concept is : `firstmile/<version>/<vendor>/data/<device-id>`
The first version is called `poc1`. This string `poc1` is in the topic hierarchy as well as in the protobuf definition.

Additional "Data Receivers" can either use one of the reference implementation provided or develop their own solution. Contributions of additional implementations of "Data Receivers" are welcome.

