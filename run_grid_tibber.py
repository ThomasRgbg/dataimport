

import dateutil
import datetime
import time

from influxdb_cli2.influxdb_cli2 import influxdb_cli2
from grid_tibber.get_tibber_data import get_tibber_data

from config_data import *

influxdb = influxdb_cli2(influxdb_url, influxdb_token, influxdb_org, influxdb_bucket, debug=False)

while True:

    tibber = get_tibber_data(tibber_ACCESS_TOKEN, influxdb)
    
    tibber.run()
    
    time.sleep(2 * 60 * 60)
