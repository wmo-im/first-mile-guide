from protospy import firstmile_pb2
from google.protobuf.json_format import Parse
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import ParseDict
import json
import os

path_oberservers = "../../standard/examples/example_schema_binding/observer.json"
path_host = "../../standard/examples/example_schema_binding/host.json"
path_parameters = "../../standard/examples/example_schema_binding/parameters.json"
path_namespaces = "../../standard/examples/example_schema_binding/namespaces.json"

output_dir = "../../standard/examples/example_output"
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
observers = read_config_json(path_oberservers, firstmile_pb2.ObserverDevice)
parameter_definitions = read_config_json(path_parameters, firstmile_pb2.ParameterDefinition)
namespace_definitions = read_config_json(path_namespaces, firstmile_pb2.Metadata.NamespacesEntry)
# read host bindings
with open(path_host, "r") as f:
    binding_json = f.read()
    host = firstmile_pb2.HostDevice()
    Parse(binding_json, host)

# generate internal observations
observations = []
internal_observation = firstmile_pb2.Observation()
internal_observation.parameterDefinitionId = 1
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
    observation.parameterDefinitionId = 2
    observation.values.extend([
        firstmile_pb2.Value(doubleValue=2304.54),
        firstmile_pb2.Value(doubleValue=12.3),
        firstmile_pb2.Value(doubleValue=1.2),
        firstmile_pb2.Value(intValue=232),

        firstmile_pb2.Value(boolValue=True)
    ])
    observations.append(observation)

# create transmission payload with observations only
data_message = firstmile_pb2.Data()
data_message.version = 1
data_message.observations.extend(observations)

# generate data message
serialized_data_message =  data_message.SerializeToString()
print(f"Length of data message: {len(serialized_data_message)}")
with open(f"{output_dir}/data_message.json", "w") as f:
    json_str = json.loads(MessageToJson(data_message))
    f.write(json.dumps(json_str, indent=4, ensure_ascii=False))

# add metadata
metadata_message = firstmile_pb2.Metadata()
metadata_message.version = 1
metadata_message.host.CopyFrom(host)
metadata_message.observers.extend(observers)
metadata_message.parameterDefinitions.extend(parameter_definitions)
metadata_message.namespaces.update({ns.key: ns.value for ns in namespace_definitions})

# generate output with metadata
serialized_with_metadata = metadata_message.SerializeToString()
print(f"Length of metadata message: {len(serialized_with_metadata)}")
with open(f"{output_dir}/metadata_message_with_metadata.json", "w") as f:
    json_str = json.loads(MessageToJson(metadata_message))
    f.write(json.dumps(json_str, indent=4, ensure_ascii=False))