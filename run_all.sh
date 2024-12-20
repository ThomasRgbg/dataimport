#!/bin/bash

set -m 

python3 run_grid_tibber.py &
python3 run_solcast.py &
python3 cal_pwr_day.py &
python3 run_engergyforcast.py &


