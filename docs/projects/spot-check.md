# Spot check spotter

This tool is built to fetch simply the latest information from the spotter including battery, humidity, power and lat long. Since these spotter can move across multiple time zones, it uses the lat long to estimate the time zone and converts the UTC time to local time for the spotter.

![pyspotter_spotcheck](https://github.com/open-oceans/pyspotter/assets/6677629/cad35989-fd95-40eb-bd7d-bd58dfb56c18)

```
pyspotter spot-check -h

usage: pyspotter spot-check [-h] --sid SID

optional arguments:
  -h, --help  show this help message and exit

Required named arguments.:
  --sid SID   Spotter ID
```

Example usage would be

```
pyspotter spot-check --sid 1484
```
