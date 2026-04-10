# Terminology and Language Conventions

Standardized terminology for WMO First-Mile documentation.

## Mandatory Terms (from Glossary)

Use these exact terms throughout the standard:

| Term | Definition | Don't Use Instead |
|------|------------|-------------------|
| **Data Sender** | The device at the remote site that collects and sends data (datalogger or sensor) | transmitter, client, publisher, source |
| **Data Receiver** | Software at central server that receives data | server, subscriber, backend, consumer |
| **Protocol** | IP-based set of rules for data transfer | transport, communication method |
| **Data Format** | Organization of information according to specifications | encoding, structure |
| **Data Serialization** | Converting structured data to transmittable format | encoding, marshalling |
| **Data Schema** | Formal declarative description of structure | schema definition, format spec |
| **Observation** | Single measurement data point | reading, sample, measurement |
| **Metadata** | Contextual information about site, sensors, parameters | configuration, setup, description |
| **Host Device** | The data sender device itself (datalogger) | host, main device, controller |
| **Observer Device** | Individual sensor connected to host | sensor, observer, detector |

## Modal Verbs (RFC 2119 Style)

For normative requirements, use precise modal verbs:

| Verb | Meaning | Usage |
|------|---------|-------|
| **shall** | Mandatory requirement | "The Data Sender shall encode observations using Protobuf" |
| **shall not** | Mandatory prohibition | "Missing values shall not be encoded as zero" |
| **should** | Recommendation | "Metadata should be sent after configuration changes" |
| **should not** | Not recommended | "Implementations should not cache metadata indefinitely" |
| **may** | Optional/permitted | "The Data Sender may send multiple observations per message" |
| **can** | Capability/possibility | "The schema can represent multiple value types" |

## Protobuf-Specific Terms

| Term | Usage Example |
|------|---------------|
| **message** | "The Data message contains observations" (capitalize when referring to specific type) |
| **field** | "The `time` field uses google.protobuf.Timestamp" |
| **repeated field** | "A repeated field that may contain zero or more values" |
| **optional field** | "An optional field that may be omitted" |
| **oneof field** | "A oneof field where exactly one option is set" |
| **enum** | "The CellMethod enum defines aggregation types" |
| **map** | "A map field containing key-value pairs" |

## Writing Style Guidelines

### Be Precise About Message Types

✅ Good:
- "The Data message contains a repeated field of Observation messages"
- "Each ParameterDefinition has a unique identifier"
- "The Value message uses a oneof field to represent different types"

❌ Avoid:
- "The data contains observations" (ambiguous: message or concept?)
- "Parameters have IDs" (which parameters?)
- "Values can be different types" (too vague)

### Use Active Voice for Requirements

✅ Good:
- "The Data Sender shall transmit observations using MQTT"
- "Implementations shall use emptyValue for missing data"

❌ Avoid:
- "Observations are transmitted using MQTT" (by whom?)
- "emptyValue is used for missing data" (passive, unclear who does this)

### Distinguish Normative from Informative

**Normative** (requirements):
- Use "shall", "shall not"
- Testable and verifiable
- Required for conformance

**Informative** (guidance):
- Use "typically", "for example", "may"
- Explanatory and educational
- Helps understanding but not required

Example:
```
Normative: "The observation field shall contain at least one Value message."
Informative: "Typically, an observation contains a single value, but multiple 
values may be used for compound measurements such as latitude/longitude pairs."
```

### Number Formatting

- **Integers**: No decimal point (e.g., "5 seconds", "100 observations")
- **Decimals**: Use appropriate precision (e.g., "-40.2°C", "latitude: -90.0")
- **Units**: Include space before unit abbreviation (e.g., "10 m", "3.5 Hz")
- **Unitless**: No space (e.g., "QoS=1", "version=1")

### Time References

- **Specific**: "2025-05-06T12:39:30.000000Z" (ISO 8601)
- **Generic**: "timestamp", "time instant", "observation time"
- **Duration**: "30 seconds", "5-minute averaging period"
- **Frequency**: "1 Hz transmission", "every 5 minutes"

### Field Reference Format

When documenting protobuf fields:

Format: `MessageType.fieldName`

Examples:
- "The `Observation.parameterDefinitionId` field references..."
- "Set `DeviceRef.observerId` to match..."
- "The `Parameter.cellMethod` enum specifies..."

### Code and Identifiers

- **Message names**: PascalCase, backticks: `ParameterDefinition`
- **Field names**: camelCase, backticks: `cellPeriodSeconds`
- **Enum values**: UPPER_SNAKE_CASE, backticks: `MEAN_ABSOLUTE_VALUE`
- **Package names**: lowercase.dot.separated: `wmo.firstmile.poc1`

## Common Phrases and Patterns

### Introducing a Concept

```
The [concept name] provides [purpose/capability]. It consists of [components].
```

Example:
```
The ParameterDefinition groups related measurement parameters. It consists of 
an identifier, a description, and a list of Parameter messages.
```

### Describing Cardinality

| Cardinality | Phrasing |
|-------------|----------|
| Required (1) | "The message shall contain a [field name]" |
| Optional (0..1) | "The message may contain a [field name]" |
| Repeated (0..*) | "The message contains zero or more [field names]" |
| Repeated non-empty (1..*) | "The message shall contain at least one [field name]" |

### Referencing Other Sections

```
As described in <<section-anchor>>
See <<section-anchor>> for details
For [topic], refer to <<section-anchor>>
```

### Listing Constraints

Use numbered or bulleted lists with "shall":

```
The Data Sender shall:

1. Encode messages using Protocol Buffers version 3
2. Transmit messages via MQTT
3. Use QoS level 1 for data messages
```

## Abbreviations and Acronyms

First use: spell out with abbreviation in parentheses
Subsequent uses: abbreviation only

Example:
```
First: "The Automatic Weather Station (AWS) collects..."
Later: "Each AWS transmits observations..."
```

| Term | Full Form | Notes |
|------|-----------|-------|
| AWS | Automatic Weather Station | |
| CF | Climate and Forecast | Metadata convention |
| GL | Ground Level | Reference surface |
| MQTT | Message Queuing Telemetry Transport | |
| MSL | Mean Sea Level | Reference surface |
| PoC | Proof of Concept | |
| WIGOS | WMO Integrated Global Observing System | |
| WMO | World Meteorological Organization | |

## Common Mistakes to Avoid

| Mistake | Correction |
|---------|------------|
| "data is sent" | "data are sent" (data is plural) OR "the Data message is sent" |
| "metadata is" | "metadata are" (plural) OR "the Metadata message is" |
| "the proto file" | "the protobuf schema" or "firstmile.proto" |
| "JSON format" | "Protobuf format" (examples shown as JSON for readability) |
| "sensor data" | "observation data" or "measurements" |
| "config" | "configuration" (spell out in formal text) |
| "missing value is null" | "missing value uses emptyValue" |

## Section-Specific Language

### Scope Section

- Use present tense: "This standard specifies..."
- Be concise: one or two paragraphs
- State what is covered and what is not

### Normative References

- Use full titles
- Include publication dates
- Format: "Organization. Title. Date. URL"

### Terms and Definitions

- Use definition lists in AsciiDoc
- Start with the term in bold
- Definition follows in plain text
- Add notes if needed for clarity

### Conformance Section

- Group requirements into classes
- Each class has a URI identifier
- Use "Requirements Class" heading style
- List dependencies on other classes

### Technical Content (Clause 5+)

- Structure: Overview → Details → Examples
- Use diagrams where helpful
- Include normative statements (shall/should)
- Provide informative examples
- Cross-reference related sections
