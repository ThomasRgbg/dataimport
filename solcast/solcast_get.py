
import dateutil
import datetime
import time

from pysolcast.rooftop import RooftopSite

def solcast_get(api_key, resource_id, influxdb): 

    site = RooftopSite(api_key, resource_id)

    forecasts = site.get_forecasts()

    # forecasts_test = {'forecasts': [{'pv_estimate': 5.1912, 'pv_estimate10': 5.1912, 'pv_estimate90': 5.1912, 'period_end': '2023-01-07T10:00:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 5.7199, 'pv_estimate10': 5.7199, 'pv_estimate90': 5.7199, 'period_end': '2023-01-07T10:30:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 5.9958, 'pv_estimate10': 5.9958, 'pv_estimate90': 5.9958, 'period_end': '2023-01-07T11:00:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 6.1641, 'pv_estimate10': 5.4418, 'pv_estimate90': 6.1641, 'period_end': '2023-01-07T11:30:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 5.845, 'pv_estimate10': 5.4127, 'pv_estimate90': 6.0835, 'period_end': '2023-01-07T12:00:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 4.6938, 'pv_estimate10': 3.0606, 'pv_estimate90': 5.8827, 'period_end': '2023-01-07T12:30:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 3.5191, 'pv_estimate10': 1.0852, 'pv_estimate90': 5.3869, 'period_end': '2023-01-07T13:00:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 2.713, 'pv_estimate10': 0.6262, 'pv_estimate90': 4.7988, 'period_end': '2023-01-07T13:30:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 2.5252, 'pv_estimate10': 0.4027, 'pv_estimate90': 4.214, 'period_end': '2023-01-07T14:00:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 2.1093, 'pv_estimate10': 0.2353, 'pv_estimate90': 3.2355, 'period_end': '2023-01-07T14:30:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 1.3165, 'pv_estimate10': 0.1265, 'pv_estimate90': 1.921, 'period_end': '2023-01-07T15:00:00.0000000Z', 'period': 'PT30M'}, {'pv_estimate': 0.145, 'pv_estimate10': 0.0253, 'pv_estimate90': 0.197, 'period_end': '2023-01-07T15:30:00.0000000Z', 'period': 'PT30M'}]}

    # forecasts = forecasts_test

    for forecast in forecasts['forecasts']:
        dt_timestamp = dateutil.parser.parse(forecast['period_end'])
        pv_estimate = forecast['pv_estimate']
        
        print(dt_timestamp, pv_estimate)
    
        influxdb.write_sensordata('solcast', 'pv_estimate', forecast['pv_estimate']*1000, dt_timestamp)
        influxdb.write_sensordata('solcast', 'pv_estimate10', forecast['pv_estimate10']*1000, dt_timestamp)
        influxdb.write_sensordata('solcast', 'pv_estimate90', forecast['pv_estimate90']*1000, dt_timestamp)

    # Delay to get DB action executed.    
    time.sleep(5)

    # print(influxdb.query_data('solcast', 'pv_estimate', datetime.datetime.utcnow()+datetime.timedelta(days=-1000), datetime.datetime.utcnow()+datetime.timedelta(days=1000)) )
    

    
