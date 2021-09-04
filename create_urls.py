import bisect
import random
import csv
import os
import sys
import urllib.request
import lzma
import math
import argparse

parser = argparse.ArgumentParser(description='Create a urls.txt for siege.')
parser.add_argument('--maxzoom', type=int, default=19, help='Maximum zoom level, inclusive.')
parser.add_argument('--bbox', type=str,help='Bounding box: min_lon,min_lat,max_lon,max_lat')
args = parser.parse_args()

def _xy(lon,lat):
    x = lon/360.0 + 0.5
    sinlat = math.sin(math.radians(lat))
    y = 0.5 - 0.25 * math.log((1.0 + sinlat) / (1.0 - sinlat)) / math.pi
    return x,y

bounds = None

if args.bbox:
    min_lon, min_lat, max_lon, max_lat = args.bbox.split(',')
    min_x, min_y = _xy(float(min_lon),float(min_lat))
    max_x, max_y = _xy(float(max_lon),float(max_lat))
    bounds = [min_x,max_y,max_x,min_y] # invert Y

# one week of anonymized tile edge request logs from openstreetmap.org
FILENAME = 'tiles-2021-08-08.txt.xz'
OUTPUT_ROWS = 10000

if not os.path.isfile(FILENAME):
    print("Downloading " + FILENAME)
    urllib.request.urlretrieve(f'https://planet.openstreetmap.org/tile_logs/{FILENAME}', FILENAME)

# output should be pseudorandom + deterministic.
random.seed(3857)

maxzoom = 19
distribution = [2,2,6,12,16,27,38,41,49,56,72,71,99,135,135,136,102,66,37,6] # the total distribution...

counts = {}
for zoom in range(maxzoom+1):
    counts[zoom] = 0

aggregate = 0
ranges = []
tiles = []

with lzma.open(FILENAME,'rt') as f:
    reader = csv.reader(f,delimiter=' ')
    for row in reader:

        split = row[0].split('/')
        z = int(split[0])
        x = int(split[1])
        y = int(split[2])

        if bounds:
            f = 1 << z
            if (x >= math.floor(bounds[0] * f) and
               x <= math.floor(bounds[2] * f) and
               y >= math.floor(bounds[1] * f) and
               y <= math.floor(bounds[3] * f)):
                pass

        count = int(row[1])
        counts[z] = counts[z] + count

        tiles.append(row[0])
        ranges.append(aggregate)
        aggregate = aggregate + count

max_count = max(counts.values())
for zoom, count in counts.items():
    p1 = ' ' if zoom < 10 else ''
    p2 = ' ' * (len(str(max_count)) - len(str(count)))
    bar = '█' * math.ceil(count / max_count * 20)
    print(f"{p1}{zoom} | {p2}{count} {bar}")

with open('urls.txt','w') as f:
    f.write("PROT=http\n")
    f.write("HOST=localhost\n")
    f.write("PORT=8080\n")
    f.write("PATH=\n")
    f.write("EXT=pbf\n")
    for sample in range(OUTPUT_ROWS):
        rand = random.randrange(aggregate)
        i = bisect.bisect(ranges,rand)-1
        f.write(f"$(PROT)://$(HOST):$(PORT)/$(PATH){tiles[i]}.$(EXT)\n")
print(f"wrote urls.txt with {OUTPUT_ROWS} requests.")
