import csv
import lzma
import math
import json

def _lonlat(z,x,y):
    z2 = math.pow(2,z)
    lon_deg = (x+0.5) / z2 * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y + 0.5) / z2)))
    lat_deg = math.degrees(lat_rad)
    return {'zoom':z,'lon':lon_deg,'lat':lat_deg}

# one week of anonymized tile edge request logs from openstreetmap.org
FILENAME = 'tiles-2021-08-08.txt.xz'

samples = []

with lzma.open(FILENAME,'rt') as f:
    reader = csv.reader(f,delimiter=' ')
    for row in reader:

        split = row[0].split('/')
        z = int(split[0])
        x = int(split[1])
        y = int(split[2])
        count = int(row[1])
        if count > 10000:
            samples.append(_lonlat(z,x,y))

print(json.dumps(samples))

