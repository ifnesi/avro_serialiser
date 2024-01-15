import os
import json
import time
import configparser

from glob import glob
from importlib import import_module
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

from utils import generate_input, ser_argparse


if __name__ == "__main__":
    args = ser_argparse(schema_type="avro")

    # Read schema file
    schema_folder, schema_base_name = os.path.split(args.schema)
    with open(args.schema, "r") as f:
        schema = json.loads(f.read())
        schema_str = json.dumps(schema)

    # Schema Registry client
    config_data = configparser.ConfigParser()
    config_data.read(args.config)
    schema_registry_client = SchemaRegistryClient(dict(config_data["schema-registry"]))

    # AVRO Serialiser object
    avro_serializer = AvroSerializer(
        schema_registry_client,
        schema_str,
    )

    # Protobuf Serialiser object
    schema_name, _ = os.path.splitext(schema_base_name)

    try:
        schema_proto = import_module(f"{schema_folder}.{schema_name}_pb2")
        protobuf_serializer = ProtobufSerializer(
            schema_proto.Proto,
            schema_registry_client,
            {
                "use.deprecated.format": False,
            },
        )
    except Exception:
        schema_proto = None
        protobuf_serializer = None

    # Generate messages
    len_message = 0
    len_message_serialised_avro = 0
    len_message_serialised_proto = 0

    if args.source_folder is not None:
        is_range = False
        list_data = glob(f"{args.source_folder}/*")
    else:
        is_range = True
        list_data = range(args.records)

    for item in list_data:
        if is_range:
            message = generate_input(schema)
            message_str = json.dumps(message)
        else:
            message_str = open(item, "r").read()
            message = json.loads(message_str)

        message_serialised = avro_serializer(
            message,
            SerializationContext(
                schema_base_name,
                MessageField.VALUE,
            ),
        )

        try:
            message_serialised_proto = protobuf_serializer(
                schema_proto.Proto(**message),
                SerializationContext(
                    f"{schema_base_name}-proto",
                    MessageField.VALUE,
                ),
            )
        except Exception:
            message_serialised_proto = ""

        if args.print:
            print(message_str)
            print(f"Avro: {message_serialised}")
            print(f"Protobuf: {message_serialised_proto}\n")

        if args.stats:
            len_message += len(message_str.encode("utf-8"))
            len_message_serialised_avro += len(message_serialised)
            len_message_serialised_proto += len(message_serialised_proto)

        if args.save:
            file_name = os.path.join(
                "data", f"{schema_base_name}-{int(time.time()*1000000)}"
            )
            with open(f"{file_name}.json", "w") as f:
                f.write(message_str)
            with open(f"{file_name}.bin", "wb") as f:
                f.write(message_serialised)

    if args.stats:
        print(f"\nRecord(s) Avro serialised: {args.records}")
        print(f"\nInput records:")
        print(f"- Total: {len_message} bytes")
        print(f"- Average per record: {len_message/args.records:0.2f} bytes")
        print(f"\nAvro serialised/encoded records:")
        print(f"- Total: {len_message_serialised_avro} bytes")
        print(
            f"  > Compress ratio: {100 * (1 - len_message_serialised_avro / len_message):0.2f}%"
        )
        print(f"\nProtobuf serialised/encoded records:")
        print(f"- Total: {len_message_serialised_proto} bytes")
        print(
            f"  > Compress ratio: {100 * (1 - len_message_serialised_proto / len_message):0.2f}%"
        )
