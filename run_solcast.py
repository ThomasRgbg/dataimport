

import dateutil
import datetime
import time

from influxdb_cli2.influxdb_cli2 import influxdb_cli2
from solcast.solcast_get import solcast_get
from pysolcast import exceptions

from config_data import *

influxdb = influxdb_cli2(influxdb_url, influxdb_token, influxdb_org, influxdb_bucket, debug=False)

while True:

    try:
        solcast_get(solcast_api_key, solcast_resource_id, influxdb)
    except exceptions.RateLimitExceeded:
        time.sleep(4 * 60 * 60)
    
    time.sleep(2 * 60 * 60)
