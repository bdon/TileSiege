![siege](https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Fotothek_df_tg_0000158_Belagerung_%5E_Festung_%5E_Belagerungsmaschine.jpg/225px-Fotothek_df_tg_0000158_Belagerung_%5E_Festung_%5E_Belagerungsmaschine.jpg)

Generates realistic traffic for load testing tile servers. Useful for:

* Measuring throughput, latency and concurrency of your tile serving stack.
* Identifying bottlenecks such as network, disk I/O, filesystem, CPU.

You could benchmark using random tiles instead, but [70% of those will be ocean.](https://en.wikipedia.org/wiki/Water_distribution_on_Earth)

# How to use

Install [siege](https://github.com/JoeDog/siege) via `apt install siege` or another package manager.

Create a urls.txt from anonymized tile requests to [openstreetmap.org](https://openstreetmap.org) for the week of 2021-08-08:

```
python create_urls.py [--bbox=MIN_LON,MIN_LAT,MAX_LON,MAX_LAT] [--maxzoom=19]
``` 

The output urls.txt will contain about 10,000 rows, with server parameters you can edit:

```
PROT=http
HOST=localhost
PORT=8080
PATH=
EXT=pbf
$(PROT)://$(HOST):$(PORT)/$(PATH)9/271/168.$(EXT)
$(PROT)://$(HOST):$(PORT)/$(PATH)9/264/186.$(EXT)
...
```

Then run your load test:

```
siege --file=urls.txt
```

 The frequency distribution of zooms will match the real data:

```
 0 |   2122775 █
 1 |   2216794 █
 2 |   6397943 █
 3 |  12472472 ██
 4 |  16428098 ███
 5 |  27779242 █████
 6 |  38843942 ██████
 7 |  41504547 ███████
 8 |  49778705 ████████
 9 |  56767305 █████████
10 |  72384991 ███████████
11 |  71587598 ███████████
12 |  99260380 ███████████████
13 | 135358540 ████████████████████
14 | 135036605 ████████████████████
15 | 136459409 ████████████████████
16 | 102903474 ████████████████
17 |  66522472 ██████████
18 |  37851474 ██████
19 |   6217710 █
```

# Notes

* The sequence of requests generated will not exhibit the same spatial correlation as real users panning and zooming.
