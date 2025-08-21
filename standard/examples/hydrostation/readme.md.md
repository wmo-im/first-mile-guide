# Hydrological Station Example

This example simulates a simple hydrological gauging station.  
**Host:** the host/datalogger purely acts as a gateway, does not provide any internal diagnostics or measurements and metadata does not contain any specific info about the host device. 
**Observers:** Geolux Radar (water level) + OTT Pluvio² (rainfall).  


**Key Points:**
- Measures critical hydrological parameters: water level and rainfall intensity.
- Data grouped under a single parameter definition since all values represent hydrological measurements.
- Metadata is minimal, there is no firmware version or serial number information from the observer instruments.
- The sample Data payload contains three measurements taken 10 minutes apart.
