# Message Structure Quick Reference

This reference provides templates for documenting the protobuf messages in AsciiDoc format.

## Message Documentation Template

```asciidoc
==== MessageName

[description of what this message represents]

[cols="1,1,1,3"]
|===
|Field |Type |Cardinality |Description

|fieldName
|TypeName
|required/optional/repeated
|Description of the field and its purpose

|===

[Optional: Additional notes, constraints, or examples]
```

## Data Message

The primary message containing observation measurements.

**Fields:**
- `observations` (repeated Observation) - List of measurement observations

**Usage**: Sent frequently with current/batched measurement data

## Metadata Message

Configuration and context information for the data sender.

**Fields:**
- `host` (HostDevice) - The data sender device
- `observers` (repeated ObserverDevice) - Connected sensor devices
- `parameterDefinitions` (repeated ParameterDefinition) - Parameter metadata
- `namespaces` (map<string, string>) - Namespace URI mappings

**Usage**: Sent on startup and when configuration changes

## Observation Message

A single measurement point.

**Fields:**
- `parameterDefinitionId` (uint32) - References a ParameterDefinition
- `time` (google.protobuf.Timestamp) - When measured
- `values` (repeated Value) - The measurement value(s)

**Notes:**
- Multiple values per observation supported (e.g., lat/lon pair)
- Each observation has independent timestamp
- Parameter ID must match a defined ParameterDefinition

## Value Message (oneof)

Polymorphic value container.

**Possible types:**
- `floatValue` (float)
- `doubleValue` (double)
- `intValue` (int32)
- `unsignedIntValue` (uint32)
- `int64Value` (int64)
- `unsignedInt64Value` (uint64)
- `stringValue` (string)
- `boolValue` (bool)
- `emptyValue` (google.protobuf.Empty) - Indicates missing/unavailable data

**Critical**: Use `emptyValue` for missing data, NOT zero, NOT omission, NOT NaN

## HostDevice Message

Describes the data sender (datalogger/station).

**Fields:**
- `name` (string) - Device model/type name
- `location` (optional Location) - Physical location
- `url` (optional string) - Link to device metadata
- `serialNumber` (optional string) - Device serial number
- `firmwareVersion` (optional string) - Firmware version

## ObserverDevice Message

Describes individual sensors.

**Fields:**
- `id` (uint32) - Unique identifier within this station
- `name` (string) - Sensor model/type name
- `location` (optional Location) - Physical location
- `url` (optional string) - Link to sensor metadata
- `serialNumber` (optional string) - Sensor serial number
- `firmwareVersion` (optional string) - Firmware version

**Notes:**
- ID must be unique among observers for this host
- Referenced by ParameterDefinition.device.observerId

## Location Message

Geographic position information.

**Fields:**
- `latitude` (optional double) - Decimal degrees
- `longitude` (optional double) - Decimal degrees
- `heightMeter` (double) - Height above reference surface
- `referenceSurface` (ReferenceSurface enum) - Height reference

**Notes:**
- Lat/lon can be omitted if only local height is known
- Height is always in meters
- Reference surface must be specified

## ParameterDefinition Message

Groups related measurement parameters.

**Fields:**
- `id` (uint32) - Unique identifier
- `description` (string) - Human-readable description
- `parameters` (repeated Parameter) - The parameter specifications

**Usage:**
- Referenced by Observation.parameterDefinitionId
- Groups parameters that share context
- Reduces redundancy in observation messages

## Parameter Message

Specification of a measurable variable.

**Fields:**
- `longName` (string) - Descriptive name (e.g., "Air Temperature")
- `unit` (string) - Unit of measurement (e.g., "°C", "m/s")
- `standardNames` (map<string, string>) - Standard name mappings
- `device` (DeviceRef) - Which device measures this
- `cellMethod` (CellMethod enum) - Aggregation method
- `cellPeriodSeconds` (uint32) - Averaging period (0 for POINT)

**Standard Names:**
- Keys must match namespace keys in Metadata.namespaces
- Common: "cf" for CF conventions, "wigos" for WIGOS identifiers
- Example: `{"cf": "air_temperature"}`

## DeviceRef Message (oneof)

References either host or observer device.

**Options:**
- `host` (google.protobuf.Empty) - Measured by the host device
- `observerId` (uint32) - Measured by observer with this ID

**Notes:**
- Exactly one must be set (oneof constraint)
- Empty host field indicates "this host device"
- Observer ID must match an ObserverDevice.id from Metadata

## CellMethod Enum

Describes data aggregation:

- `POINT` (1) - Instantaneous value
- `SUM` (2) - Sum over period
- `MAXIMUM` (3) - Maximum value
- `MINIMUM` (7) - Minimum value
- `MEAN` (9) - Average value
- `MEDIAN` (5) - Median value
- `VARIANCE` (17) - Variance
- `STANDARD_DEVIATION` (15) - Standard deviation

Plus: MAXIMUM_ABSOLUTE_VALUE, MID_RANGE, MINIMUM_ABSOLUTE_VALUE, MEAN_ABSOLUTE_VALUE, MEAN_OF_UPPER_DECILE, MODE, RANGE, ROOT_MEAN_SQUARE, SUM_OF_SQUARES

**Usage:**
- POINT means cellPeriodSeconds should be 0
- Other methods require cellPeriodSeconds > 0

## ReferenceSurface Enum

Height reference systems:

- `MSL` (1) - Mean Sea Level
- `GEOID` (2) - Geoid model
- `GL` (3) - Ground Level
- `REFERENCE_ELLIPSOID` (4) - WGS84 or similar
- `PRESSURE_1000_HPA` (5) - 1000 hPa pressure level

## AsciiDoc Formatting Examples

### Simple Field List

```asciidoc
The Observation message contains the following fields:

* `parameterDefinitionId` - The ID of the parameter being measured
* `time` - The timestamp using google.protobuf.Timestamp format
* `values` - A list of Value messages containing the measurements
```

### Table Format

```asciidoc
[cols="1,1,3"]
|===
|Field |Type |Description

|parameterDefinitionId
|uint32
|Unique identifier referencing a ParameterDefinition

|time
|google.protobuf.Timestamp
|Timestamp when the observation was made

|values
|repeated Value
|One or more measurement values

|===
```

### With Admonitions

```asciidoc
==== Missing Values

When a sensor value is unavailable (e.g., due to malfunction), the value shall be encoded using the `emptyValue` field of type `google.protobuf.Empty`.

[IMPORTANT]
====
Missing values shall NOT be encoded as:

* Zero (0)
* NaN (Not a Number)
* Omitted from the message
====
```

### Cross-Referencing

```asciidoc
The `parameterDefinitionId` field references a `ParameterDefinition` as defined in <<parameter-definition>>.

[[parameter-definition]]
==== ParameterDefinition

[description follows...]
```
