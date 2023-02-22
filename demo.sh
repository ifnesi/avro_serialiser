#!/bin/sh

clear

if [ -z "$1" ]
then
    QTY=1
else
    QTY=`expr $1 + 0`
fi
QTY=$(( $QTY < 1 ? 1 : $QTY ))

echo
echo "*** Avro weather schema ***"
cat schemas/weather.avro
echo
read -p "Press any key to see $QTY random input message(s) based on the Avro weather schema..."
echo

python3 avro_serialiser.py --qty $QTY --schema schemas/weather.avro --stats > stats.txt
cat input.json
echo
read -p "Press any key to see Avro serialised output..."
echo

cat output.avsc
echo
echo
read -p "Press any key to compare raw input with Avro serialised output..."

cat stats.txt
echo
