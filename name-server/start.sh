#! /bin/bash

# Kelvin Chris Lau, klau158, 9682466

python3 name_server.py &
python3 buffer.py &
python3 consumer.py &
python3 producer.py &