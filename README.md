# dataimport
Collection of scripts colleting data from misc services (Home centric, like weather, sunshind, grid)

- wetterdienst_get: Imports local weather data data with https://wetterdienst.readthedocs.io/en/latest/ (DWD Mosmix) and loads it into a influxdb
- solcast_get: Imports photovoltaik prediction data with https://github.com/mcaulifn/solcast (https://solcast.com/) and loads it into a influxdb
- grid_tibber: Imports current electricity price and consumption with https://github.com/Danielhiversen/pyTibber for the Tibber energy company.



