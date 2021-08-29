import bisect
import random
import csv
import sys

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
        count = int(row[1])
        split = row[0].split('/')
        z = int(split[0])
        x = int(split[1])
        y = int(split[2])
        tiles.append(row[0])
        ranges.append(aggregate)
        aggregate = aggregate + count

for sample in range(1000):
    rand = random.randrange(aggregate)
    i = bisect.bisect(ranges,rand)
    print(tiles[i])


