
#
# Device Database and registry
#

# Need to be adapted to your local devices.
# And these values here are just default values, not my ones... ;)

mqtt_ip = "192.168.0.10"
mqtt_port = 1883
mqtt_topic = "home/heizung"

influxdb_url = 'http://192.168.0.10:8086'
influxdb_token = "putyourtokenhere"
influxdb_org = 'home'
influxdb_bucket = 'home/autogen'

influxdb_price_location = 'grid_tibber'
influxdb_price_measurement = 'price_total'

tibber_ACCESS_TOKEN = "mytibbertocken"
 
solcast_api_key = 'mysolcastkey'
solcast_resource_id = 'mysolcastresource'
