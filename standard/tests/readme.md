# Tests Directory
Place to store the source data accumulated to enable testing of the First Mile Schema [Issue 45].  Testing is about:
- flexibility of the Schema to accomodate the broad range of data that needs to be communicated
- resilience/robustness of (Receiver) implementations to handle
  - broad range of data types
  - errors/issues/corner cases in implemetnations

## Flexibility
| Discrete Sampling Geometry Type | Point |  timeSeries | trajectory | profile | timeSeriesProfile |
|---------|----------|---------- |---------- |---------- |---------- |
| Description [from NetCDF CF conventions] | A single data point (having no implied coordinate relationship to other points)  | A series of data points at the same spatial location with time values in strict monotonically increasing order | A series of data points along a path through space with time values in strict monotonically increasing order | An ordered set of data points along a vertical line a a fixed horizontal position and fixed time |  A series of profile features at the same horizontal position with time values in strict monotonically increasing order |
| Value 3 | Value 4  | VAlue 5 | VAlue 5 | VAlue 5 | VAlue 5 |


