import uuid
import random
import string
import argparse
import datetime


# General functions
def int_min(records: str, min_value: int = 1):
    if not str(records).isdigit():
        raise argparse.ArgumentTypeError("Must be an integer point number")
    elif int(records) < min_value:
        raise argparse.ArgumentTypeError(f"Argument must be >= {min_value}")
    return int(records)


def generate_input(avro_schema: dict) -> dict:
    """Very basic random generate function for AVRO schemas (it accepts nested/complex schemas)"""
    result = dict()
    if isinstance(avro_schema, dict):
        if avro_schema.get("type") == "record":
            for field in avro_schema.get("fields", list()):
                field_name = field.get("name")
                field_type = field.get("type")
                logical_type = field.get("logicalType")

                # Randomly pick one tield type if many
                if isinstance(field_type, (tuple, list)):
                    field_type = random.choice(field_type)

                # Generate random input

                # STRING
                if field_type == "string":
                    if logical_type == "uuid":
                        data = str(uuid.uuid4())
                    else:
                        data = "".join(
                            random.choices(
                                string.printable[:62], k=random.randint(4, 10)
                            )
                        )

                # INT
                elif field_type == "int":
                    if logical_type == "date":
                        data = random.randint(
                            0,
                            (
                                datetime.datetime.utcnow()
                                - datetime.datetime(1970, 1, 1)
                            ).days,
                        )
                    elif logical_type == "time-millis":
                        now = datetime.datetime.utcnow()
                        data = 1000 * (
                            now.time().hour * 3600
                            + now.time().minute * 60
                            + now.time().second
                        )
                    else:
                        data = random.randint(1000, 9999)

                # FLOAT
                elif field_type == "float":
                    data = random.random() * 1000

                # DOUBLE
                elif field_type == "double":
                    data = random.randint(1000, 99999) / 100

                # LONG
                elif field_type == "long":
                    if logical_type == "timestamp-millis":
                        data = int(datetime.datetime.utcnow().timestamp() * 1000)
                    elif logical_type == "timestamp-micros":
                        data = int(datetime.datetime.utcnow().timestamp() * 1000000)
                    elif logical_type == "time-micros":
                        now = datetime.datetime.utcnow()
                        data = 1000000 * (
                            now.time().hour * 3600
                            + now.time().minute * 60
                            + now.time().second
                        )
                    else:
                        data = random.randint(10000000, 99999999)

                # BOOLEAN
                elif field_type == "boolean":
                    data = random.random() >= 0.5

                # RECORD
                elif field_type == "record":
                    data = generate_input(field)

                # NULL
                else:
                    data = None

                result.update({field_name: data})

    return result
