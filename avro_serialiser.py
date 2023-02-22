import os
import sys
import json
import argparse
import fastavro

from utils import int_min, generate_input


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AVRO encoder")
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
        help=f"Avro schema file name",
        default=os.path.join("schemas", "weather.avro"),
    )
    parser.add_argument(
        "--output",
        dest="output",
        type=str,
        help=f"Filename where the encoded Avro data should be dumped to",
        default="output.avsc",
    )
    parser.add_argument(
        "--input",
        dest="input",
        type=str,
        help=f"Filename where the randomised input data should be dumped to",
        default="input.json",
    )
    parser.add_argument(
        "--stats",
        dest="stats",
        help=f"Display statistics",
        action="store_true",
    )
    args = parser.parse_args()

    # Parse Avro schema
    if not os.path.isfile(args.schema):
        print(f"\nERROR: Avro schema not found: {args.schema}\n")
        sys.exit(0)

    with open(args.schema, "r") as f:
        schema = json.loads(f.read())
        parsed_schema = fastavro.parse_schema(schema)

    # Generate random input and avro compress them
    records = list()
    avro_overhead_size = 0
    for i in range(args.records):
        # Generate random input
        record = generate_input(schema)
        records.append(record)

        # Dump input random record to disk
        with open(args.input, "w" if i == 0 else "a") as f:
            f.write(f"{json.dumps(record)}\n")

        # Estimate size of avro schema overhead
        if i == 0:
            test_records = list()
            for n in range(2):
                test_records.append(record)
                with open(args.output, "wb") as out:
                    fastavro.writer(
                        out,
                        parsed_schema,
                        test_records,
                    )
                total_file_size = os.path.getsize(args.output)
                if n == 0:
                    # File with schema (overhead) and one record
                    avro_overhead_size = total_file_size
                else:
                    # File with schema (overhead) and two records (same initial record but twice)
                    avro_overhead_size = 2 * avro_overhead_size - total_file_size

    # Avro serialise and save to file (final output)
    with open(args.output, "wb") as out:
        fastavro.writer(
            out,
            parsed_schema,
            records,
        )

    if args.stats:
        # Calculate statistics
        raw = os.path.getsize(args.input)
        avg_raw = raw / args.records
        serialised = os.path.getsize(args.output)
        avro_data_size = serialised - avro_overhead_size
        avg_avro_schema = serialised / args.records
        avg_avro = avro_data_size / args.records

        # Display statistics
        print(f"\nRecord(s) serialised: {args.records}")
        print(f"\nInput records:")
        print(f"- Total: {raw} bytes")
        print(f"- Average per record: {avg_raw:0.2f} bytes")
        print(f"\nAvro serialised/encoded records:")
        print(f"- Total: {serialised} bytes")
        print(f"- Record average size with Avro schema: {avg_avro_schema:0.2f} bytes")
        print(f"  > Compress ratio: {100 * (1 - serialised / raw):0.2f}%")
        print(f"- Record average size without Avro schema: {avg_avro:0.2f} bytes")
        print(f"  > Compress ratio: {100 * (1 - avg_avro / avg_raw):0.2f}%\n")
