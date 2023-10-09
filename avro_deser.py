import os
import glob
import argparse
import configparser

from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AVRO deserialiser")
    parser.add_argument(
        "--config",
        dest="config",
        help=f"Configuration file to access the Schema Registry cluster (default 'config/test.ini')",
        default=os.path.join("config", "test.ini"),
    )
    parser.add_argument(
        "--schema",
        dest="schema",
        type=str,
        help=f"avro Schema file path",
        default=None,
    )
    args = parser.parse_args()

    # Schema Registry client
    config_data = configparser.ConfigParser()
    config_data.read(args.config)
    schema_registry_client = SchemaRegistryClient(dict(config_data["schema-registry"]))

    # AVRO Deserialiser object
    avro_deserializer = AvroDeserializer(
        schema_registry_client,
        schema_str=None if args.schema is None else open(args.schema, "r").read(),
    )

    # Read messages
    for file in glob.glob(os.path.join("data", "*.bin")):
        topic = "-".join(os.path.basename(file).split("-")[:-1])
        with open(file, "rb") as f:
            message_serialised = f.read()
            message_deserialised = avro_deserializer(
                message_serialised,
                SerializationContext(
                    topic,
                    MessageField.VALUE,
                ),
            )

        print(f"File: {file}")
        print(message_serialised)
        print(f"{message_deserialised}\n")
