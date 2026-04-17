This test captures a field scenario first proposed by Niksa Orlic

A simple AWS is set up with Temperature, Humidity and Pressure sensors and starts reporting.
The Pressure Sensor fails and for a time only Temperature and Humidity are reported.
The Technician goes to site to repair the Pressure Sensor, but also takes the opportunity to add a Wind Sensor.  
In their eagerness to get the Wind Sensor going, data is sent from the 4 sensors (Temperature, Humidity, Pressure, Wind) but the MetatData file is not sent until the Tech realises their error.
The correct MetatData File is then sent and the AWS reports correctly.

The key part of this test is how the Receiver handles the data received from the 4 sensors, when they only have a Metadata message for 3 sensors.
