#!/bin/sh

clear

if [ -z "$1" ]
then
    QTY=1
else
    QTY=`expr $1 + 0`
fi
QTY=$(( $QTY < 1 ? 1 : $QTY ))

echo "Avro weather schema:"
cat schemas/weather.avro
echo
read -p "Press any key to see $QTY random input message(s) based on the Avro weather schema and stats..."
echo

python3 avro_ser.py --qty $QTY --schema schemas/weather.avro --stats --print
