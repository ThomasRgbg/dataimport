
#from numpy import datetime64, timedelta64, isnan
import datetime

from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest, DwdMosmixType
from wetterdienst import Settings


#def convert_dt64_to_dt(dt64):
    #unix_epoch = datetime64(0, 's')
    #one_second = timedelta64(1, 's')
    #seconds_since_epoch = (dt64 - unix_epoch) / one_second
    #return datetime.datetime.utcfromtimestamp(seconds_since_epoch)


def wetterdienst_get(influxdb):

    Settings.tidy = True

    request = DwdMosmixRequest(
        mosmix_type=DwdMosmixType.SMALL,
        parameter=["TTT", 'FF', 'RR1c', 'Neff', 'SunD1', 'Rad1h', 'VV', 'wwM'],
        start_date=(datetime.date.today().isoformat()),
        end_date=((datetime.date.today()  + datetime.timedelta(7)).isoformat()),
    )

    stations = request.filter_by_station_id(station_id=["P551", "10776", "P366", "P441", "P449", "P460", "N0680"],)

    for response in stations.values.query():

        print(dir(response))
        print(response)

    # next2days = response.df[0:48]

        for i in range(len(response.df)):
            
            # print(response.df["parameter"].values[i])
            # continue
            
            value = response.df["value"][i]

            if not value:
                continue
            #if isnan(value):
            #    continue

            date = response.df["date"][i]

            if response.df["station_id"][i] == "10776":
                location = "weatherforcast"
            elif response.df["station_id"][i] == "P551":
                location = "weatherforcast_langquaid"
            elif response.df["station_id"][i] == "P460":
                location = "weatherforcast_hagelstadt"
            elif response.df["station_id"][i] == "P366":
                location = "weatherforcast_schwandorf"
            elif response.df["station_id"][i] == "P441":
                location = "weatherforcast_parsberg"
            elif response.df["station_id"][i] == "P449":
                location = "weatherforcast_kelheim"
            elif response.df["station_id"][i] == "N0680":
                location = "weatherforcast_germersheim"
            else:
                continue
            
            if response.df["parameter"][i] == 'temperature_air_mean_200':
                influxdb.write_sensordata(location, "temperature_2m", value - 273.15, date)

            if response.df["parameter"][i] == 'wind_speed':
                influxdb.write_sensordata(location, "windspeed", value * 3.6, date)

            if response.df["parameter"][i] == 'precipitation_height_significant_weather_last_1h':
                influxdb.write_sensordata(location, "rain", value, date)

            if response.df["parameter"][i] == 'cloud_cover_effective':
                influxdb.write_sensordata(location, "cloudcover", value, date)

            if response.df["parameter"][i] == 'sunshine_duration':
                influxdb.write_sensordata(location, "sunshine", value, date)

            if response.df["parameter"][i] == 'radiation_global':
                influxdb.write_sensordata(location, "radiation_all", value, date)

            if response.df["parameter"][i] == 'visibility_range':
                influxdb.write_sensordata(location, "visibility", value, date)

            if response.df["parameter"][i] == 'probability_fog_last_1h':
                influxdb.write_sensordata(location, "propability_fog", value, date)

    print("Done")
