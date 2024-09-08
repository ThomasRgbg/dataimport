import asyncio

import aiohttp
import tibber

import dateutil
import datetime
import time

class get_tibber_data:
    def __init__(self, apikey, influxdb):
        self.apikey = apikey
        self.influxdb = influxdb

        self.power_average_seconds = 10
        self.power_average_count = 0
        self.power_average = 0
        self.power_average_start_timestamp = datetime.datetime.now()
        self.power_sum_seconds = 300 / self.power_average_seconds
        self.power_sum_count = 0

    def _callback(self, pkg):

        data = pkg.get("data")
        if data is None:
            print("No Callback data none")
            return
        realtimedata = data.get("liveMeasurement")
        # print(realtimedata)
        # print('Realtime power={0}, powerProduction={1}'.format(realtimedata['power'],realtimedata['powerProduction']))
        power = realtimedata['power'] - realtimedata['powerProduction']

        dt_timestamp = dateutil.parser.parse(realtimedata['timestamp'])

        if self.power_average_count == 0:
            self.power_average = float(power)
            self.power_average_start_timestamp = datetime.datetime.now()
        else:
            self.power_average += power
        
        self.power_average_count += 1
        
        # print(self.power_average_count, self.power_average, self.power_average_start_timestamp)
        
        if datetime.datetime.now() - self.power_average_start_timestamp > datetime.timedelta(seconds = self.power_average_seconds):
            power_sum = self.power_average / self.power_average_count
            self.power_average_count = 0
            self.power_sum_count += 1

            dt_timestamp = dateutil.parser.parse(realtimedata['timestamp'])
            self.influxdb.write_sensordata("grid_tibber", "meter_power", power_sum , dt_timestamp)

            if self.power_sum_count > self.power_sum_seconds:
                self.power_sum_count = 0
                self.influxdb.write_sensordata("grid_tibber", "meter_comsumption", realtimedata['lastMeterConsumption'] , dt_timestamp)
                self.influxdb.write_sensordata("grid_tibber", "meter_production", realtimedata['lastMeterProduction'] , dt_timestamp)
        
    async def main(self):
        async with aiohttp.ClientSession() as session:
            tibber_connection = tibber.Tibber(self.apikey, websession=session, user_agent="my_pyTibber_useage")
            await tibber_connection.update_info()
            print(tibber_connection.name)
            home = tibber_connection.get_homes()[0]
            await home.update_info()
            await home.update_price_info()
            #if not home.rt_subscription_running:
            await home.rt_subscribe(self._callback)

            await asyncio.sleep(10)

            while(True):
                
                await home.update_info_and_price_info()

                print(dir(home))
                print(home.home_id)
                # print(home.has_real_time_consumption)
                # print(home.current_price_info)

                prices = home.price_total

                for timestamp in prices:
                    dt_timestamp = dateutil.parser.parse(timestamp)
                    # print("{0} - {1}".format(dt_timestamp, prices[timestamp]))

                    self.influxdb.write_sensordata("grid_tibber", "price_total", prices[timestamp] , dt_timestamp)

                await asyncio.sleep(60*30)

    def run(self):
        asyncio.run(self.main())

