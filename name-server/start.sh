#! /bin/bash

python3 name_server.py &
python3 buffer.py &
python3 consumer.py &
python3 producer.py &