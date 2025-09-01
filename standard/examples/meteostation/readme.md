# Hydrometeorological Station Example

This example shows a typical automatic weather station located in central Europe.  
**Host:** Campbell CR3000 recording weather data plus internal system status.
**Observers:** Vaisala WXT536 measuring meteorological parameters.  


**Key Points:**
- Weather parameters: air temperature, humidity, pressure, wind, rainfall.
- Datalogger monitors battery voltage, solar input, and logger temperature.
- Data block groups meteorological parameters and logger health separately.
- This example sends emptyValue for the barometer pressure measurement which indicates that the corresponing sensor did not succesfully provide a reading. This may indicate a sensor fault, and the receiver must skip this Value.
