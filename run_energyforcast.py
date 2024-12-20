#!/usr/bin/env python3

# based on https://github.com/mampfes/ha_epex_spot/blob/main/custom_components/epex_spot/test_energyforecast.py

import aiohttp
import asyncio
import datetime

from energyforcast.energyforcast import Energyforecast

from config_data import *
from influxdb_cli2.influxdb_cli2 import influxdb_cli2

influxdb = influxdb_cli2(influxdb_url, influxdb_token, influxdb_org, influxdb_bucket, debug=False)


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            service = Energyforecast(market_area="DE-DE", token=energyforcast_api_key, session=session)

            await service.fetch()
            print(f"energyforcast: count = {len(service.marketdata)}")
            for e in service.marketdata:
                print(f"energyforcast: {e.start_time}: {e.price_per_kwh}")
                # print(type(e.start_time))
                # timestamp = datetime.datetime.fromisoformat(str(e.start_time))
                influxdb.write_sensordata("grid_tibber", "price_forcast", e.price_per_kwh , e.start_time)

            await asyncio.sleep(120*60)


asyncio.run(main())
