 
import asyncio
import time
import datetime
import statistics

from influxdb_cli2.influxdb_cli2 import influxdb_cli2
from config_data import *


influxdb = influxdb_cli2(influxdb_url, influxdb_token, org=influxdb_org, bucket=influxdb_bucket) # debug=args.debug
influxdb_table = 'pv_prediction'

def get_predicted_power(mode=None):
    if mode == "today":
        now = datetime.datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    elif mode == "tomorrow":
        now = datetime.datetime.now()+datetime.timedelta(days=1)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    elif mode == "dayaftertomorrow":
        now = datetime.datetime.now()+datetime.timedelta(days=2)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    elif mode == "remaining":
        now = datetime.datetime.now()
        start = now
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    else:
        return 0, 0, []
    
    
    results = influxdb.query_data('solcast', 'pv_estimate', start, end)
    if results == []:
        return 0, 0, []
    elif results:
        values = []
        lenght = 0
        pwr = 0
#        print(results[:][:])
        for i in results:
            values.append(i[3])
            pwr += i[3]
            lenght += 1
            
        # since one datapoint per 30 min
        pwr /= 2
        return pwr, lenght, values
    else:
        return 0, 0, []


def get_collected_power(mode=None):
    if mode == "today":
        now = datetime.datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    else:
        return 0
        
    results = influxdb.query_data('pv_fronius', 'MPPT_1_DC_Energy', start, start + datetime.timedelta(minutes=1))
    if results == []:
        return 0, 0, 0
    elif results:
        start1 = results[0][3]
    else:
        return 0, 0, 0
    

    results = influxdb.query_data('pv_fronius', 'MPPT_1_DC_Energy',  end + datetime.timedelta(hours=-12), end)
    if results == []:
        return 0, 0, 0
    elif results:
        stop1 = results[-1][3]
    else:
        return 0, 0, 0

    results = influxdb.query_data('pv_fronius', 'MPPT_2_DC_Energy', start, start + datetime.timedelta(minutes=1))
    if results == []:
        return 0, 0, 0
    elif results:
        start2 = results[0][3]
    else:
        return 0, 0, 0
    

    results = influxdb.query_data('pv_fronius', 'MPPT_2_DC_Energy',  end + datetime.timedelta(hours=-12), end)
    if results == []:
        return 0, 0, 0
    elif results:
        stop2 = results[-1][3]
    else:
        return 0, 0, 0

    return (stop1-start1), (stop2-start2), (stop1-start1) + (stop2-start2)

while(True):

    pwr, lenght, values = get_predicted_power('today')
    pwr_remaining, lenght, values = get_predicted_power('remaining')

    mppt1, mppt2, mppt_both = get_collected_power('today')

    influxdb.write_sensordata(influxdb_table, 'prediction_today', pwr, force=False)
    influxdb.write_sensordata(influxdb_table, 'prediction_remaining', pwr_remaining, force=False)
    influxdb.write_sensordata(influxdb_table, 'generated_today', mppt_both, force=False)

    time.sleep(30*60)
    
#
