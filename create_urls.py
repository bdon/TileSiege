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
parser.add_argument('--minzoom', type=int, default=0, help='Minimum zoom level, inclusive.')
parser.add_argument('--maxzoom', type=int, default=19, help='Maximum zoom level, inclusive.')
parser.add_argument('--bbox', type=str,help='Bounding box: min_lon,min_lat,max_lon,max_lat')
args = parser.parse_args()

def _xy(lon,lat):
    x = lon/360.0 + 0.5
    sinlat = math.sin(math.radians(lat))
    y = 0.5 - 0.25 * math.log((1.0 + sinlat) / (1.0 - sinlat)) / math.pi
    return x,y

def percentage_split(size, percentages):
    prv = 0
    cumsum = 0
    for zoom, p in percentages.items():
        cumsum += p
        nxt = int(cumsum * size)
        yield zoom, prv, nxt
        prv = nxt

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

minzoom = args.minzoom
maxzoom = args.maxzoom
distribution = [2,2,6,12,16,27,38,41,49,56,72,71,99,135,135,136,102,66,37,6] # the total distribution...

total_weight = 0
totals = {}
ranges = {}
tiles = {}
for zoom in range(minzoom, maxzoom+1):
    total_weight = total_weight + distribution[zoom]
    totals[zoom] = 0
    ranges[zoom] = []
    tiles[zoom] = []

with lzma.open(FILENAME,'rt') as f:
    reader = csv.reader(f,delimiter=' ')
    for row in reader:

        split = row[0].split('/')
        z = int(split[0])
        x = int(split[1])
        y = int(split[2])
        count = int(row[1])

        if z < minzoom or z > maxzoom:
            continue

        if bounds:
            f = 1 << z
            if (x >= math.floor(bounds[0] * f) and
               x <= math.floor(bounds[2] * f) and
               y >= math.floor(bounds[1] * f) and
               y <= math.floor(bounds[3] * f)):
                pass
            else:
                continue

        ranges[z].append(totals[z])
        tiles[z].append(row[0])
        totals[z] = totals[z] + count

with open('urls.txt','w') as f:
    f.write("PROT=http\n")
    f.write("HOST=localhost\n")
    f.write("PORT=8080\n")
    f.write("PATH=\n")
    f.write("EXT=pbf\n")
    rows = 0
    for zoom, start, end in percentage_split(
        OUTPUT_ROWS, {zoom: distribution[zoom] / total_weight for zoom in range(minzoom, maxzoom + 1)}
    ):
        rows_for_zoom = end - start
        rows += rows_for_zoom
        for sample in range(rows_for_zoom):
            rand = random.randrange(totals[zoom])
            i = bisect.bisect(ranges[zoom],rand)-1
            f.write(f"$(PROT)://$(HOST):$(PORT)/$(PATH){tiles[zoom][i]}.$(EXT)\n")
        p1 = ' ' if zoom < 10 else ''
        p2 = ' ' * (len(str(10000)) - len(str(rows_for_zoom)))
        bar = '█' * math.ceil(rows_for_zoom / OUTPUT_ROWS * 60)
        print(f"{p1}{zoom} | {p2}{rows_for_zoom} {bar}")
print(f"wrote urls.txt with {rows} requests.")
