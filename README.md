# avro_serialiser

Avro serialiser/deserialiser using Python and Confluent AVRO SerDes lib (`confluent_kafka.schema_registry.avro`).

It will also serialise using Confluent Protobuf SerDes lib for comparison.

## Installation and Configuration
- Python +3.8 required
- Install python virtual environment: ```python3 -m pip install venv```
- Clone this repo: ```git git@github.com:ifnesi/avro_serialiser.git```
- Go to the folder where the repo was cloned: ```cd avro_serialiser```
- Create a virtual environment: ```python3 venv _venv```
- Activate the virtual environment: ```source _venv/bin/activate```
- Install project requirements: ```python3 -m pip install -f requirements.txt```
- Deactivate the virtual environment: ```deactivate```

## AVRO Serialiser
```
usage: avro_ser.py [-h] [--qty RECORDS] [--schema SCHEMA] [--stats] [--print] [--save] [--config CONFIG]

AVRO serialiser

options:
  -h, --help       show this help message and exit
  --qty RECORDS    Quantity of input records to be randomised (based on the Avro schema)
  --config CONFIG  Configuration file to access the Schema Registry cluster (default 'config/test.ini')
  --schema SCHEMA  Avro schema file path
  --stats          Display statistics
  --print          Print messages in the console
  --save           Save serialised data to folder 'data/'
```

## AVRO Deserialiser
```
usage: avro_deser.py [-h] [--config CONFIG] [--schema SCHEMA]

AVRO deserialiser

options:
  -h, --help       show this help message and exit
  --config CONFIG  Configuration file to access the Schema Registry cluster (default 'config/test.ini')
  --schema SCHEMA  avro Schema file path
```

## Running the demo (serialiser):
Run the shell script: ```./demo.sh {qty}```
- Where `qty` (Optional):
  - Number of random input messages to be generated using the schemas/weather.avro schema
  - qty >= 1 (default is 1)

Output example:
```
% ./demo.sh 1

Avro weather schema:
{
    "name": "Weather",
    "namespace": "com.example",
    "doc": "My weather station",
    "type": "record",
    "fields": [
        {
            "name": "station",
            "type": "string"
        },
        {
            "name": "station_id",
            "type": "long"
        },
        {
            "name": "timestamp",
            "type": "long",
            "logicalType": "timestamp-millis"
        },
        {
            "name": "temp",
            "type": "double"
        },
        {
            "name": "active",
            "type": "boolean"
        }
    ]
}

Press any key to see 1 random input message(s) based on the Avro weather schema and stats...

{"station": "klkb8t5l9", "station_id": 36791040, "timestamp": 1696839823769, "temp": 250.36, "active": true}
Avro: b'\x00\x00\x01\x86\xc0\x12klkb8t5l9\x80\x8c\x8b#\xb2\xc6\xc7\xb8\xe2b\xecQ\xb8\x1e\x85Ko@\x01'
Protobuf: b'\x00\x00\x01\x86\xc2\x00\n\tklkb8t5l9\x10\x80\xc6\xc5\x11\x18\x99\xe3\xa3\x9c\xb11!\xecQ\xb8\x1e\x85Ko@(\x01'


Record(s) Avro serialised: 1

Input records:
- Total: 108 bytes
- Average per record: 108.00 bytes

Avro serialised/encoded records:
- Total: 34 bytes
  > Compress ratio: 68.52%

Protobuf serialised/encoded records:
- Total: 40 bytes
  > Compress ratio: 62.96%
```

## Running the demo (deserialiser):
Run the python script: ```python3 avro_deser.py```

Output example:
```
File: data/weather.avro-1696843423938279.bin
b'\x00\x00\x01\x86\xc0\x12klkb8t5l9\x80\x8c\x8b#\xb2\xc6\xc7\xb8\xe2b\xecQ\xb8\x1e\x85Ko@\x01'
{'station': 'klkb8t5l9', 'station_id': 36791040, 'timestamp': 1696839823769, 'temp': 250.36, 'active': True}
```

To understand how the field alias work on Avro schemas, for example, see the schema `schemas/weather_alias.avro` below. When compare to the schema `schemas/weather.avro` you will notice the field `station` is now an alias and the new field name (from the consumer's perspective) is `station_name`
```
{
    "name": "Weather",
    "namespace": "com.example",
    "doc": "My weather station",
    "type": "record",
    "fields": [
        {
            "name": "station_name",  <--- New field name (by the consumer's perspective)
            "aliases": ["station"],  <--- List of aliases (original field name when serialising the event)
            "type": "string"
        },
        {
            "name": "station_id",
            "type": "long"
        },
        {
            "name": "timestamp",
            "type": "long",
            "logicalType": "timestamp-millis"
        },
        {
            "name": "temp",
            "type": "double"
        },
        {
            "name": "active",
            "type": "boolean"
        }
    ]
}
```

Now run again the python script but this time add the `--schema` parameter: ```python3 avro_deser.py --schema schemas/weather_alias.avro```

Output example:
```
File: data/weather.avro-1696843423938279.bin
b'\x00\x00\x01\x86\xc0\x12klkb8t5l9\x80\x8c\x8b#\xb2\xc6\xc7\xb8\xe2b\xecQ\xb8\x1e\x85Ko@\x01'
{'station_name': 'klkb8t5l9', 'station_id': 36791040, 'timestamp': 1696839823769, 'temp': 250.36, 'active': True}
```

The field `station` has been renamed by the comnsumer to `station_name` even though it was originnaly serialised as `station`