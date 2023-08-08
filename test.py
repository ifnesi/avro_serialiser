import io
import json
import random
import struct
import avro.datafile
import avro.schema
import avro.io
import avro.ipc

SCHEMA = avro.schema.Parse(
    json.dumps(
        {
            "namespace": "example.avro",
            "type": "record",
            "name": "User",
            "fields": [
                {"name": "name", "type": "string"},
                {"name": "favorite_number", "type": ["int", "null"]},
                {"name": "favorite_color", "type": ["string", "null"]},
            ],
        }
    )
)


def send_message(message):
    buf = io.BytesIO()
    writer = avro.datafile.DataFileWriter(buf, avro.io.DatumWriter(), SCHEMA)
    writer.append(message)
    writer.flush()
    data_length = buf.tell()
    buf.seek(0)
    data = buf.read()
    bytes_written = struct.pack("!L", data_length)
    print("Wrote bytes", bytes_written)
    bytes_written = data
    print("Wrote bytes", bytes_written)


def main():
    names = ["Nick", "Scott", "Josh", "Anusha", "Eli"]
    colors = ["red", "green", "blue", "black", "fuscia"]
    for _ in range(20):
        send_message(
            {
                "name": random.choice(names),
                "favorite_number": random.randint(0, 100),
                "favorite_color": random.choice(colors),
            },
        )


if __name__ == "__main__":
    main()
