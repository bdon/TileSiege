import csv
import os
import sys
import urllib.request
import lzma
import argparse
import datetime
from collections import Counter

parser = argparse.ArgumentParser(description='Create a urls.txt for siege.')
args = parser.parse_args()


today = datetime.date.today() - datetime.timedelta(days=2)
dates = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(89)]

for date in dates:
    filename = 'tiles-' + date + '.txt.xz'
    if not os.path.isfile('data/' + filename):
        print("Downloading " + filename)
        urllib.request.urlretrieve(f'https://planet.openstreetmap.org/tile_logs/' + filename, 'data/' + filename)

counter = Counter()

for date in dates:
    filename = 'tiles-' + date + '.txt.xz'
    with lzma.open('data/' + filename,'rt') as f:
        reader = csv.reader(f,delimiter=' ')
        for row in reader:
            counter[row[0]] += int(row[1])

for t in counter.most_common(100000):
    print(t[0])

