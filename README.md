# avro_serialiser

Basic Avro serialiser using Python:
```
usage: avro_serialiser.py [-h] [--qty RECORDS] [--schema SCHEMA] [--output OUTPUT] [--input INPUT] [--stats]

AVRO encoder

options:
  -h, --help       show this help message and exit
  --qty RECORDS    Quantity of input records to be randomised (based on the Avro schema)
  --schema SCHEMA  Avro schema file name
  --output OUTPUT  Filename where the encoded Avro data should be dumped to
  --input INPUT    Filename where the randomised input data should be dumped to
  --stats          Display statistics
```

## Installation and Configuration
- Python +3.8 required
- Install python virtual environment: ```python3 -m pip install venv```
- Clone this repo: ```git git@github.com:ifnesi/avro_serialiser.git```
- Go to the folder where the repo was cloned: ```cd avro_serialiser```
- Create a virtual environment: ```python3 venv _venv```
- Activate the virtual environment: ```source _venv/bin/activate```
- Install project requirements: ```python3 -m pip install -f requirements.txt```
- Deactivate the virtual environment: ```deactivate```

## Running the demo:
- Run the shell script: ```./demo.sh X```
- Where X (Optional):
  - Number of random input messages to be generated using the schemas/weather.avro schema
  - X >= 1 (default is 1)

Example:
```
% ./demo.sh 1

*** Avro weather schema ***
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

Press any key to see 1 random input message(s) based on the Avro weather schema...

{"station": "tivtALIh7", "station_id": 66385658, "timestamp": 1677077421574, "temp": 453.69, "active": false}

Press any key to see Avro serialised output...

Objavro.codenullavro.schema�{"type": "record", "doc": "My weather station", "name": "com.example.Weather", "fields": [{"name": "station", "type": "string"}, {"name": "station_id", "type": "long"}, {"logicalType": "timestamp-millis", "name": "timestamp", "type": "long"}, {"name": "temp", "type": "double"}, {"name": "active", "type": "boolean"}]}���f������w�y:tivtALIh7�ۧ?��ԙ�aףp=
[|@���f������w�y

Press any key to compare raw input with Avro serialised output...

Record(s) serialised: 1

Input records:
- Total: 110 bytes
- Average per record: 110.00 bytes

Avro serialised/encoded records:
- Total: 417 bytes
- Record average size with Avro schema: 417.00 bytes
  > Compress ratio: -279.09%
- Record average size without Avro schema: 29.00 bytes
  > Compress ratio: 73.64%
```