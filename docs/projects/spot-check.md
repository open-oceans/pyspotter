# Spot check spotter

This tool is built to fetch simply the latest information from the spotter including battery, humidity, power and lat long. Since these spotter can move across multiple time zones, it uses the lat long to estimate the time zone and converts the UTC time to local time for the spotter.

![pyspotter_check](https://user-images.githubusercontent.com/6677629/147421383-6b8f16a0-b3ab-481f-ad2d-b3be15407b34.gif)

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
pyspotter spot-check --sid 0320
```
