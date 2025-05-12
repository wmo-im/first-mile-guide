from protospy import firstmile_pb2
from google.protobuf.json_format import Parse
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import ParseDict
import json
import os

path_oberservers = "./sample_config/observers.json"
path_host = "./sample_config/host.json"
path_parameters = "./sample_config/parameters.json"

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

def read_config_json(json_path, schema):
    """Load list of protobuf message objects from a JSON config file."""
    bindings = []
    with open(json_path, "r") as f:
        bindings_json = json.load(f)
        for binding in bindings_json["bindings"]:
            new_binding = schema()
            ParseDict(binding, new_binding)
            bindings.append(new_binding)
    return bindings

# load and parse bindings for devices and parameters
observers = read_config_json(path_oberservers, firstmile_pb2.Device)
parameter_definitions = read_config_json(path_parameters, firstmile_pb2.ParameterDefinition)
# read host bindings
with open(path_host, "r") as f:
    binding_json = f.read()
    host = firstmile_pb2.Device()
    Parse(binding_json, host)

# generate internal observations
observations = []
internal_observation = firstmile_pb2.Observation()
internal_observation.parameter_id = 1
internal_observation.time.GetCurrentTime()
internal_observation.values.extend([
    firstmile_pb2.Value(doubleValue=12.9),
    firstmile_pb2.Value(doubleValue=33.28)
])
observations.append(internal_observation)

# generate 3 random observations
for i in range(3):
    observation = firstmile_pb2.Observation()
    observation.time.GetCurrentTime()
    observation.parameter_id = 2
    observation.values.extend([
        firstmile_pb2.Value(doubleValue=2304.54),
        firstmile_pb2.Value(doubleValue=12.3),
        firstmile_pb2.Value(doubleValue=1.2),
        firstmile_pb2.Value(intValue=232),

        firstmile_pb2.Value(boolValue=True)
    ])
    observations.append(observation)

# create transmission payload with observations only
transmission = firstmile_pb2.Transmission()
transmission.hostId = "TT-1M"
transmission.observations.extend(observations)

# generate output without metadata
serialized_wo_metadata = transmission.SerializeToString()
print(f"Length without metadata: {len(serialized_wo_metadata)}")
with open(f"{output_dir}/transmission_wo_metadata.json", "w") as f:
    json_str = json.loads(MessageToJson(transmission))
    f.write(json.dumps(json_str, indent=4, ensure_ascii=False))

# add metadata
transmission.host.CopyFrom(host)
transmission.observers.extend(observers)
transmission.parameterDefinitions.extend(parameter_definitions)

# generate output with metadata
serialized_with_metadata = transmission.SerializeToString()
print(f"Length with metadata: {len(serialized_with_metadata)}")
with open(f"{output_dir}/transmission_with_metadata.json", "w") as f:
    json_str = json.loads(MessageToJson(transmission))
    f.write(json.dumps(json_str, indent=4, ensure_ascii=False))