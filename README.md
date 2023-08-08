# avro_serialiser

Avro serialiser/deserialiser using Python and Confluent AVRO SerDes lib (`confluent_kafka.schema_registry.avro`):

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
usage: avro_deser.py [-h] [--config CONFIG]

AVRO deserialiser

options:
  -h, --help       show this help message and exit
  --config CONFIG  Configuration file to access the Schema Registry cluster (default 'config/test.ini')
```

## Running the demo (serialiser):
- Run the shell script: ```./demo.sh {qty}```
- Where `qty` (Optional):
  - Number of random input messages to be generated using the schemas/weather.avro schema
  - qty >= 1 (default is 1)

Example:
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

{"station": "m2ygG", "station_id": 64310212, "timestamp": 1691490475617, "temp": 774.0, "active": true}
b'\x00\x00\x01\x86\xc0\nm2ygG\x88\xaf\xaa=\xc2\xf9\x82\xcb\xbab\x00\x00\x00\x00\x000\x88@\x01'


Record(s) serialised: 1

Input records:
- Total: 103 bytes
- Average per record: 103.00 bytes

Avro serialised/encoded records:
- Total: 30 bytes
  > Compress ratio: 70.87%
```

## Running the demo (deserialiser):
- Run the python script: ```python3 avro_deser.py```

Example:
```
File: data/weather.avro-1691493709833374.bin
b'\x00\x00\x01\x86\xc0\nm2ygG\x88\xaf\xaa=\xc2\xf9\x82\xcb\xbab\x00\x00\x00\x00\x000\x88@\x01'
{"station": "m2ygG", "station_id": 64310212, "timestamp": 1691490475617, "temp": 774.0, "active": true}
```
