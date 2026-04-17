# Tests Directory
Place to store the source data accumulated to enable testing of the First Mile Schema [Issue 45].  Testing is about:
- flexibility of the Schema to accomodate the broad range of data that needs to be communicated
- resilience/robustness of (Receiver) implementations to handle
  - broad range of data types
  - errors/issues/corner cases in implemetnations

## Flexibility
[thanks to David Inglis Berry for this framework]

| Discrete Sampling Geometry Type | Point |  timeSeries | trajectory | profile | timeSeriesProfile |
|---------|----------|---------- |---------- |---------- |---------- |
| Description [from NetCDF CF conventions] | A single data point (having no implied coordinate relationship to other points)  | A series of data points at the same spatial location with time values in strict monotonically increasing order | A series of data points along a path through space with time values in strict monotonically increasing order | An ordered set of data points along a vertical line a a fixed horizontal position and fixed time |  A series of profile features at the same horizontal position with time values in strict monotonically increasing order |
| Weather |   | [first-mile-guide/standard/tests/flexibility/weather/timeSeries](./flexibility/weather/timeSeries/BOM_AWS)  | [first-mile-guide/standard/tests/flexibility/weather/trajectory/AMDAR](./flexibility/weather/trajectory/AMDAR) |  |  |
| Cryosphere |   |  |  |  |  |
| Hydrology |   |[first-mile-guide/standard/tests/flexibility/hydrology/timeSeries](./flexibility/hydrology/timeSeries/BWA)   |  |  |  |
| Atmospheric Composition |   |  |[first-mile-guide/standard/tests/flexibility/atmospheric_composition/trajectory](./flexibility/atmospheric_composition/trajectory)  |  |  |
| Oceans |   |  |  |  |  |

## Resilience/Robustness

| Test | Test Aim | Folder |
| ----- | ----- | -----|
| Implementation Completeness| First Mile Schema and Sample data that uses all the possible values in the schema to check a Receiver Implementation has covered all the possible content values| [first-mile-guide/standard/tests/resilience/completness](./resilience/completeness) |
| Misaligned MetaData| Short scenario whereby data is sent before the correct MetaData| [first-mile-guide/standard/tests/resilience/misaligned_metadata](./resilience/misaligned_metadata) |
