

import dateutil
import datetime
import time

from influxdb_cli2.influxdb_cli2 import influxdb_cli2
from wetterdienst_get.wetterdienst_influxdb import wetterdienst_get

from config_data import *

influxdb = influxdb_cli2(influxdb_url, influxdb_token, influxdb_org, influxdb_bucket, debug=False)

while True:

    wetterdienst_get(influxdb)
    
    time.sleep(1 * 60 * 60)
