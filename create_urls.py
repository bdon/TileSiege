import bisect
import random
import csv
import os
import sys
import urllib.request
import lzma
import math

# one week of anonymized tile edge request logs from openstreetmap.org
FILENAME = 'tiles-2021-08-08.txt.xz'
OUTPUT_ROWS = 10000

if not os.path.isfile(FILENAME):
    print("Downloading " + FILENAME)
    urllib.request.urlretrieve(f'https://planet.openstreetmap.org/tile_logs/{FILENAME}', FILENAME)

# output should be pseudorandom + deterministic.
random.seed(3857)

maxzoom = 19

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
        i = bisect.bisect(ranges,rand)
        f.write(f"$(PROT)://$(HOST):$(PORT)/$(PATH){tiles[i]}.$(EXT)\n")
print(f"wrote urls.txt with {OUTPUT_ROWS} requests.")


