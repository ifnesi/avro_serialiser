import os
import json
import time
import argparse
import configparser

from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from utils import int_min, generate_input


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AVRO serialiser")
    parser.add_argument(
        "--qty",
        dest="records",
        type=int_min,
        help=f"Quantity of input records to be randomised (based on the Avro schema)",
        default=1,
    )
    parser.add_argument(
        "--schema",
        dest="schema",
        type=str,
        help=f"Avro schema file path",
        default=os.path.join("schemas", "weather.avro"),
    )
    parser.add_argument(
        "--stats",
        dest="stats",
        help=f"Display statistics",
        action="store_true",
    )
    parser.add_argument(
        "--print",
        dest="print",
        help=f"Print messages in the console",
        action="store_true",
    )
    parser.add_argument(
        "--save",
        dest="save",
        help=f"Save serialised data to folder 'data/'",
        action="store_true",
    )
    parser.add_argument(
        "--config",
        dest="config",
        help=f"Configuration file to access the Schema Registry cluster (default 'config/test.ini')",
        default=os.path.join("config", "test.ini"),
    )
    args = parser.parse_args()

    # Read schema file
    schema_base_name = os.path.basename(args.schema)
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

    # Generate messages
    len_message = 0
    len_message_serialised = 0
    for i in range(args.records):
        message = generate_input(schema)
        message_str = json.dumps(message)
        message_serialised = avro_serializer(
            message,
            SerializationContext(
                schema_base_name,
                MessageField.VALUE,
            ),
        )

        if args.print:
            print(message_str)
            print(f"{message_serialised}\n")

        if args.stats:
            len_message += len(message_str.encode("utf-8"))
            len_message_serialised += len(message_serialised)

        if args.save:
            file_name = os.path.join(
                "data", f"{schema_base_name}-{int(time.time()*1000000)}"
            )
            with open(f"{file_name}.json", "w") as f:
                f.write(message_str)
            with open(f"{file_name}.bin", "wb") as f:
                f.write(message_serialised)

    if args.stats:
        print(f"\nRecord(s) serialised: {args.records}")
        print(f"\nInput records:")
        print(f"- Total: {len_message} bytes")
        print(f"- Average per record: {len_message/args.records:0.2f} bytes")
        print(f"\nAvro serialised/encoded records:")
        print(f"- Total: {len_message_serialised} bytes")
        print(
            f"  > Compress ratio: {100 * (1 - len_message_serialised / len_message):0.2f}%"
        )
