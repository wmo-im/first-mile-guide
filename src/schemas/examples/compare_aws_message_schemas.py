import datetime

import import_obs
import json
import os
import io
import subprocess

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from avro.errors import InvalidAvroBinaryEncoding

from cbor2 import dumps, dump, load
from pycddl import Schema


def write_json_schema(obs_list, filepath=""):
    json_object = json.dumps(obs_list)
    json_file = open(json_filepath, "w")
    json_file.write(json_object)
    json_file.close()

def write_avro_schema(obs_list, filepath="", schema_filepath=""):
    schema_avro = avro.schema.parse(open(schema_filepath, "rb").read())
    writer_aws = DataFileWriter(open(filepath, "wb"), DatumWriter(), schema_avro)

    for data in obs_list:
        writer_aws.append(data)

    writer_aws.close()

def read_avro_schema(filepath=""):
    reader_aws = DataFileReader(open(filepath, "rb"), DatumReader())
    return_data = []
    for data in reader_aws:
        print(data)
        return_data.append(data)
    reader_aws.close()
    return return_data

def write_avro_schemaless(obs_list, filepath="", schema_filepath=""):
    schema_avro = avro.schema.parse(open(schema_filepath, "rb").read())
    writer_lite = avro.io.DatumWriter(schema_avro)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)

    for data in obs_list:
        writer_lite.write(data, encoder)

    raw_bytes = bytes_writer.getvalue()
    schema_less_file = open(filepath, "wb")
    schema_less_file.write(raw_bytes)
    schema_less_file.close()

def read_avro_schemaless(filepath="", schema_filepath=""):
    schema_less_file = open(filepath, "rb")
    raw_bytes_in = schema_less_file.read()
    schema_less_file.close()

    bytes_reader = io.BytesIO(raw_bytes_in)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    schema_avro = avro.schema.parse(open(schema_filepath, "rb").read())
    reader = avro.io.DatumReader(schema_avro)

    read_good = True
    return_data = []

    while read_good:
        try:
            read_test = reader.read(decoder)
            print(read_test)
            return_data.append(read_test)
        except InvalidAvroBinaryEncoding:
            read_good = False

    return return_data

def write_cbor_schema(obs_list, filepath="", schema_filepath=""):
    cbor_output_file = open(filepath, 'wb')

    obs_wrapper = {"records": obs_list}
    dump(obs_wrapper, cbor_output_file)
    cbor_output_file.close()

    cbor_schema_file = open(schema_filepath, 'r')
    cbor_schema = cbor_schema_file.read()

    schema = Schema(cbor_schema)
    schema.validate_cbor(dumps(obs_wrapper))

def read_cbor(filepath=""):
    cbor_input_file = open(filepath, 'rb')
    obs_wrapper = load(cbor_input_file)
    cbor_input_file.close()

    loaded_data = obs_wrapper["records"]
    return_data = []
    for data in loaded_data:
        print(data)
        return_data.append(data)

    return return_data

# These functions help automate the setting of attributes of attributes in the ProtoBuf Object

import functools

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

# using wonder's beautiful simplification: https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects/31174427?noredirect=1#comment86638618_31174427

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))

def write_protobuf_schema(obs_list, filepath="", schema_filepath=""):
    # automate the creation of the ProtoBuf Class/Object
    base_filepath = os.path.dirname(__file__)
    f = open("proto_create2.bat", "w")
    f.write("cd .\\protoc-30.1-win64\\bin\\ \n")  # change to the directory where the protoc.exe is
    f.write(".\\protoc --proto_path=%s --python_out=%s %s \n" % (base_filepath, base_filepath, schema_filepath)) # enable the compiling by providing the relevant directories and source files

    f.close()

    result = subprocess.run([".\proto_create2.bat"], capture_output=True)
    print(result.stdout)
    print(result.stderr)

    # use the created object
    import aws_message_schema3_pb2

    message1 = aws_message_schema3_pb2.aws_message_new()

    for data in obs_list:
        aws_record = message1.records.add()

        for key in data.keys():
            if type(data[key]) is dict:
                key_stub = str(key)
                for key1 in data[key].keys():
                    key_this = key_stub + "." + key1
                    rsetattr(aws_record, key_this, data[key][key1])

            else:
                if key=="cloud":
                    for dk in data[key]:
                        aws_record.clouds.append(dk)
                else:
                    setattr(aws_record, key, data[key])

    output_proto_file = open(filepath, "wb")
    output_text = message1.SerializeToString()
    output_proto_file.write(output_text)
    output_proto_file.close()

def read_protobuf(filepath=""):
    input_proto_file = open(filepath, "rb")

    import aws_message_schema3_pb2
    message_in = aws_message_schema3_pb2.aws_message_new()

    message_in.ParseFromString(input_proto_file.read())
    return_data = []
    for record in message_in.records:
        this_record = {}

        fields = record.DESCRIPTOR.fields_by_name.keys()

        for field in fields:
            this_attr = getattr(record, field)

            try:
                this_attr_fields = this_attr.DESCRIPTOR.fields_by_name.keys()
                this_record[field] = {}
                for field_name in this_attr_fields:
                    this_record[field][field_name] = getattr(this_attr, field_name)
            except AttributeError:
                this_record[field] = this_attr

        print(this_record)

    return return_data

obs_list = import_obs.get_obs_data(filepath="new 6.txt", obs_count = 1)
obs_list_use = []
use_tags = ["station_wsi", "obs_dt_utc", "wind_speed", "wind_direction"] # wind only station example
#use_tags = ["station_wsi", "obs_dt_utc", "wind_speed", "wind_direction",  "visibility", "air_temperature",
#            "dew_point", "rel_humidity", "rainfall", "pressure", "engineering", "cloud"]  #full aviation AWS example

#take the source date/time stamps and make into milliseconds since epoch timestamp
for i in range(len(obs_list)):
    combined_dt = datetime.datetime(obs_list[i]['date'].year, obs_list[i]['date'].month, obs_list[i]['date'].day,
                                obs_list[i]['time'].hour, obs_list[i]['time'].minute, obs_list[i]['time'].second)
    obs_list[i]['obs_dt_utc'] = int(combined_dt.timestamp()*1000)
    del obs_list[i]['date']
    del obs_list[i]['time']

#reduce the provided dictionary to the tags we are going to use
for i in range(len(obs_list)):
    new_dict = {}
    for tag in use_tags:
        if tag in obs_list[i]:
                new_dict[tag] = obs_list[i][tag]

    obs_list_use.append(new_dict)


#save to JSON - used for size comparisons
json_filepath = "aws_message_json.msg"
write_json_schema(obs_list_use, filepath=json_filepath)

filesize_json = os.path.getsize(json_filepath)
print("FileSize (json):", filesize_json)

#avro schema
avro_filepath = "aws_message_avro.msg"
avro_schemaless_filepath = "aws_message_avroschemaless.msg"
avro_schema_filepath = "aws_message_schema3.avro" # wind only schema
#avro_schema_filepath = "aws_message_schema4.avro" # full AWS schema
write_avro_schema(obs_list_use, filepath=avro_filepath, schema_filepath=avro_schema_filepath)

filesize_avro = os.path.getsize(avro_filepath)
print("FileSize (avro):", filesize_avro)

write_avro_schemaless(obs_list_use, filepath=avro_schemaless_filepath, schema_filepath=avro_schema_filepath)

filesize_schemaless_avro = os.path.getsize(avro_schemaless_filepath)
print("FileSize (avro schemaless):", filesize_schemaless_avro)
filesize_schema_avro = os.path.getsize(avro_schema_filepath)
print("FileSize (avro schema):", filesize_schema_avro)

#cbor with cddl
cbor_filepath = "aws_message_cbor.msg"
cbor_cddl_schema_filepath = "aws_message_schema2.cddl"  # wind only AWS schema
#cbor_cddl_schema_filepath = "aws_message_schema3.cddl" # full AWS Schema
write_cbor_schema(obs_list_use, filepath=cbor_filepath, schema_filepath=cbor_cddl_schema_filepath)

filesize_cbor = os.path.getsize(cbor_filepath)
print("FileSize (cbor):", filesize_cbor)
filesize_cbor_schema = os.path.getsize(cbor_cddl_schema_filepath)
print("FileSize (cbor schema):", filesize_cbor_schema)

#protobuf
protobuf_filepath = "aws_message_proto.msg"
protobuf_schema_filepath = "aws_message_schema2.proto" # wind only AWS schema
#protobuf_schema_filepath = "aws_message_schema3.proto" # full AWS schema
write_protobuf_schema(obs_list_use, filepath=protobuf_filepath, schema_filepath=protobuf_schema_filepath)

filesize_proto = os.path.getsize(protobuf_filepath)
print("FileSize (protobuf):", filesize_proto)

filesize_schema_proto = os.path.getsize(protobuf_schema_filepath)
print("FileSize (protobuf schema):", filesize_schema_proto)


# now read them back
avro_data = read_avro_schema(filepath=avro_filepath)
avro_data_from_schemaless = read_avro_schemaless(filepath=avro_schemaless_filepath, schema_filepath=avro_schema_filepath)
cbor_data = read_cbor(filepath=cbor_filepath)
protobuf_data = read_protobuf(filepath=protobuf_filepath)

