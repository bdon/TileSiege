import bisect
import random
import csv
import sys
import urllib.request
import lzma
import math

# FILENAME = 'tiles-2021-08-08.txt'

# if not os.path.isfile(FILENAME):
#     urllib.request.urlretrieve(f'https://planet.openstreetmap.org/tile_logs/{FILENAME}.xz', FILENAME)

random.seed(3857)

maxzoom = 19

counts = {}
for zoom in range(maxzoom+1):
    counts[zoom] = 0

aggregate = 0
ranges = []
tiles = []

with open(sys.argv[1],'r') as f:
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

# for sample in range(1000):
#     rand = random.randrange(aggregate)
#     i = bisect.bisect(ranges,rand)
#     print(tiles[i])


