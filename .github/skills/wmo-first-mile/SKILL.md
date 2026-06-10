---
name: wmo-first-mile
description: 'Domain knowledge for WMO First-Mile Data Collection standards. Use for understanding the protobuf schema, data model concepts, message structures, protocols, terminology, and conventions specific to this standardization project.'
user-invocable: false
---

# WMO First-Mile Data Collection Standard

Domain-specific knowledge for drafting the WMO First-Mile Data Collection Guide standards documentation.

## Source of Truth

**PRIMARY REFERENCES**:
- **Protobuf Schema**: `standard/protobuf-schema/firstmile.proto` - The definitive data format specification
- **Requirements Document**: `requirements/requirements.adoc` - Complete PoC implementation requirements and technical details

**SECONDARY REFERENCES** (for understanding only, DO NOT copy into standard):
- Python examples in `reference-implementations/python-example/` - Understanding typical implementations
- C examples in `reference-implementations/c-nanopb-example/` - Low-level implementation patterns

**SKILL REFERENCES** (loaded on-demand for guidance):
- [Message Structures](./references/message-structures.md) - AsciiDoc templates and message documentation patterns
- [Terminology](./references/terminology.md) - Standardized terms, modal verbs, and writing conventions

## Project Context

This is a **WMO (World Meteorological Organization)** standardization initiative led by the First-Mile Task Team (1M-TT) to create a communication protocol for first-mile data collection from remote meteorological and hydrological observation sites.

**Key Goal**: Enable low-bandwidth, efficient transmission of observational data from remote sensors/dataloggers to central data receivers.

## Core Concepts

### Communication Model

1. **Unidirectional**: Data flows ONLY from Data Sender → Data Receiver (no two-way communication)
2. **Data Format**: Protocol Buffers (Protobuf) for efficient serialization
3. **Transport Protocol**: MQTT for message delivery
4. **Bandwidth-Constrained**: Optimized for satellite links and limited connectivity

### Key Components

- **Data Sender**: The "thing" at the remote site (weather station, datalogger, sensor) that collects and sends data
- **Data Receiver**: Central server software that receives and processes the protobuf payloads
- **Host Device**: The data sender itself (e.g., datalogger)
- **Observer Device**: Individual sensors connected to the host (e.g., temperature sensor, rain gauge)

## Data Model Structure

### Message Hierarchy

```
Data Message (sent frequently)
├── version
└── observations[]
    ├── parameterDefinitionId
    ├── time
    └── values[]

Metadata Message (sent on config changes)
├── host (HostDevice)
├── observers[] (ObserverDevice)
├── parameterDefinitions[]
│   ├── id
│   ├── description
│   └── parameters[]
│       ├── longName
│       ├── unit
│       ├── standardNames{}
│       ├── device (DeviceRef)
│       ├── cellMethod
│       └── cellPeriodSeconds
└── namespaces{}
```

### Critical Message Types

Defined in `firstmile.proto`:

1. **Data** - Container for observations (measurement data)
2. **Metadata** - Site configuration, sensors, parameter definitions
3. **Observation** - Single measurement point with parameter ID, timestamp, values
4. **Value** - Polymorphic type supporting double, int32, uint32, int64, uint64, string, bool, or empty (missing)
5. **HostDevice** - The data sender/datalogger
6. **ObserverDevice** - Individual sensors
7. **ParameterDefinition** - Groups related parameters with shared context
8. **Parameter** - Definition of a measurable variable
9. **Location** - Geographic position with reference surface
10. **DeviceRef** - Reference to either host or observer device

### CellMethod Enum

Describes how data is aggregated:
- `POINT` - Instantaneous value
- `SUM`, `MEAN`, `MAXIMUM`, `MINIMUM` - Aggregation methods
- `MEDIAN`, `MODE`, `VARIANCE`, `STANDARD_DEVIATION` - Statistical methods
- `MEAN_OF_UPPER_DECILE`, `ROOT_MEAN_SQUARE` - Advanced statistics

### ReferenceSurface Enum

Height reference systems:
- `MSL` - Mean Sea Level
- `GEOID` - Geoid reference
- `GL` - Ground Level
- `REFERENCE_ELLIPSOID` - Reference Ellipsoid
- `PRESSURE_1000_HPA` - 1000 hPa Pressure Level

## Terminology Conventions

**Use these exact terms** (from glossary in requirements.adoc):

- **Data Sender** (not "transmitter", "client", "publisher")
- **Data Receiver** (not "server", "subscriber", "backend")
- **Protocol** - IP-based transfer rules
- **Data Format** - Organization of information (Protobuf)
- **Data Schema** - Formal structure definition (the .proto file)
- **Observation** - Single measurement data point
- **Metadata** - Configuration and context information
- **Host Device** - The datalogger or primary unit
- **Observer Device** - Individual sensor

## MQTT Topic Structure

**Metadata topic**: `firstmile/[version]/[vendor_name]/metadata/hostId`
- Retain flag: 1
- QoS: 2

**Data topic**: `firstmile/[version]/[vendor_name]/data/hostId`
- Retain flag: 0
- QoS: 1

## Key Design Decisions

1. **No bidirectional communication** - Simplifies implementation for constrained devices
2. **Metadata is optional but recommended** - Can send data-only messages
3. **Missing values use emptyValue** - NOT zero, NOT omitted, NOT NaN
4. **Multiple observations per message** - Efficient batch transmission
5. **Parameter definitions group related parameters** - Context sharing
6. **StandardNames use namespace mapping** - Supports CF conventions, WIGOS, etc.
7. **No alarm/event mechanism** - Use bool values as measurements if needed

## Implementation Patterns

From requirements.adoc test cases:

1. **Event Data** (Hydrology Raingauge) - Silent with occasional heartbeat, bursts during events
2. **Batch Upload** (Argo Float) - Collect over time/space, transmit all at once
3. **High Frequency** (Aviation AWS) - 1Hz continuous transmission
4. **Dynamic Reconfiguration** - Add/remove sensors, update metadata

## Writing Guidelines

### When drafting standard sections:

1. **Be precise about message types**: "The Data message contains observations" not "data contains observations"
2. **Reference the proto schema**: Use exact field names and types from firstmile.proto
3. **Distinguish normative vs informative**: Implementation examples are informative
4. **Use proper modal verbs**:
   - "shall" for mandatory requirements
   - "should" for recommendations
   - "may" for optional features
5. **Cross-reference consistently**: Link to other clauses when mentioning related concepts
6. **Include examples**: JSON representations help readers understand the binary protobuf format

### AsciiDoc Conventions for this project:

- Use `[source,proto]` for protobuf schema blocks
- Use `[source,json]` for example data (protobuf shown as JSON for readability)
- Use definition lists for message field descriptions
- Include message hierarchy diagrams where helpful
- Use admonitions (NOTE, IMPORTANT) for implementation guidance

## Common Patterns to Document

1. **Parameter definition flow**:
   - Define in Metadata message
   - Reference by ID in Observation
   - Supports multi-value observations (multiple Values per Observation)

2. **Device attribution**:
   - Parameters link to either host or observer via DeviceRef
   - ObserverDevice has unique ID
   - HostDevice is implicit (empty field in DeviceRef)

3. **Time representation**:
   - Always use `google.protobuf.Timestamp`
   - Observations have individual timestamps
   - Supports sending multiple observations with different times

4. **Namespace resolution**:
   - Namespaces defined in Metadata.namespaces
   - Parameter.standardNames keys must match namespace keys
   - Example: `"cf": "https://vocab.nerc.ac.uk/collection/P07/current/"`

## Section-Specific Guidance

### Clause 7 (Data Model)

Should cover:
- Message structure and relationships
- Field descriptions for each message type
- Constraints and validation rules
- How parameter definitions work
- Value type handling (including missing values)
- Device hierarchy (host vs observer)
- Location and reference surfaces
- Cell methods and aggregation periods

### Example Sections (if requested)

Should include:
- Realistic use cases (AWS, hydrology station, etc.)
- Both Data and Metadata messages
- JSON representation of protobuf for readability
- Multiple observations at different times
- Proper namespace usage
- Complete parameter definitions

## Validation Checklist

Before committing documentation:

- [ ] All message types from firstmile.proto are covered
- [ ] Field names match the protobuf schema exactly
- [ ] Terminology is consistent with requirements.adoc glossary
- [ ] Examples use valid protobuf structure
- [ ] CellMethod and ReferenceSurface enums are explained
- [ ] DeviceRef oneof behavior is clear
- [ ] Missing value handling (emptyValue) is documented
- [ ] MQTT topic structure is specified correctly
- [ ] Cross-references between sections work
- [ ] AsciiDoc syntax is valid

## Quick Reference

**Message Priority**:
1. Data - Most frequently sent
2. Metadata - Sent on startup and config changes

**Field Cardinality**:
- `repeated` = array (0 or more)
- `optional` = may be omitted
- No modifier = required (but may be empty for messages)

**Naming Style**:
- Messages: PascalCase (e.g., `ParameterDefinition`)
- Fields: camelCase (e.g., `parameterDefinitionId`)
- Enums: UPPER_SNAKE_CASE (e.g., `MEAN_ABSOLUTE_VALUE`)

## How to Use This Skill

1. **Load the skill** when starting work on WMO First-Mile documentation
2. **Consult message structures** when documenting protobuf messages - load [Message Structures](./references/message-structures.md)
3. **Check terminology** for correct usage of terms and modal verbs - load [Terminology](./references/terminology.md)
4. **Verify against proto** - always cross-check field names and types in `firstmile.proto`
5. **Follow AsciiDoc patterns** from the structure reference for consistent formatting
