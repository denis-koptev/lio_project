#!/bin/bash

sudo ./wipe_system.sh

for i in {1..50}
do
	echo "Starting LIO Session #$i"
	./lio_start_session.sh lio_json_initial.json > /dev/null
	./verify_io.py session/initconf_init1_io_result
	./get_type_average.py session/initconf_init1_io_result
	./wipe_system.sh
done


