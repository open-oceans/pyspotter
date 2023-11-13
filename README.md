# pyspotter: Simple CLI for SofarOcean API

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=plastic&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/samapriya/)
[![Medium](https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white)](https://medium.com/@samapriyaroy)
[![Twitter URL](https://img.shields.io/twitter/follow/samapriyaroy?style=social)](https://twitter.com/intent/follow?screen_name=samapriyaroy)
[![Mastodon Follow](https://img.shields.io/mastodon/follow/109627075086849826?domain=https%3A%2F%2Fmapstodon.space%2F)](https://mapstodon.space/@samapriya)
[![CI pyspotter](https://github.com/samapriya/pyspotter/actions/workflows/package_ci.yml/badge.svg)](https://github.com/samapriya/pyspotter/actions/workflows/package_ci.yml)
[![Hits-of-Code](https://hitsofcode.com/github/open-oceans/pyspotter?branch=main)](https://hitsofcode.com/github/open-oceans/pyspotter?branch=main)
![PyPI - License](https://img.shields.io/pypi/l/pyspotter)
[![Downloads](https://pepy.tech/badge/pyspotter)](https://pepy.tech/project/pyspotter)
![PyPI](https://img.shields.io/pypi/v/pyspotter)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5805519.svg)](https://doi.org/10.5281/zenodo.5805519)
[![Donate](https://img.shields.io/badge/Donate-Buy%20me%20a%20Chai-teal)](https://www.buymeacoffee.com/samapriya)
[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/samapriya)


SofarOcean is creating one of the largest commercial ocean observation grids with its smart buoys (spotters) & smart mooring. Spotter delivers high-fidelity, real-time wave, wind, and temperature data from anywhere. Sofar is also focused on providing this dataset to researchers and users of the data and this tool was an attempt to simple parse spotter information. They also have an official client for doing many of these functions which can be found here [sofar-api-client-python](https://github.com/sofarocean/sofar-api-client-python). You can also find their [indepth API and documentation here](https://docs.sofarocean.com/)

This tool is an attempt to parse out some of the basic functionalities of the API including but not limited to tool like authentication protocols, token reset, and data export for easy use in other platforms like google earth engine.

#### Citation

```
Samapriya Roy. (2021). samapriya/pyspotter: Simple CLI for SofarOcean API (0.0.6).
Zenodo. https://doi.org/10.5281/zenodo.5805519
```

## Table of contents
- [pyspotter: Simple CLI for SofarOcean API](#pyspotter-simple-cli-for-sofarocean-api)
      - [Citation](#citation)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Getting started](#getting-started)
  - [pyspotter Simple CLI for Sofarocean API](#pyspotter-simple-cli-for-sofarocean-api-1)
    - [pyspotter auth](#pyspotter-auth)
    - [pyspotter reset](#pyspotter-reset)
    - [pyspotter devlist](#pyspotter-devlist)
    - [pyspotter spotcheck](#pyspotter-spotcheck)
    - [pyspotter spotdata](#pyspotter-spotdata)
  - [Changelog](#changelog)
      - [v0.0.5](#v005)
      - [v0.0.4](#v004)
      - [v0.0.3](#v003)
      - [v0.0.2](#v002)


## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

**pyspotter only support Python v3.4 or higher**

To install **pyspotter: Simple CLI for SofarOcean API** you can install using two methods.

```pip install pyspotter```

or you can also try

```
git clone https://github.com/samapriya/pyspotter.git
cd pyspotter
python setup.py install
```
For Linux use sudo or try ```pip install pyspotter --user```.

I recommend installation within a virtual environment. Find more information on [creating virtual environments here](https://docs.python.org/3/library/venv.html).

## Getting started

As usual, to print help:

```
pyspotter -h
usage: pyspotter [-h] {auth,reset,devlist,spot-check,spot-data} ...

Simple CLI for Sofarocean API

positional arguments:
  {auth,reset,devlist,spot-check,spot-data}
    auth                Authenticates and saves your API token
    reset               Regenerates your API token
    devlist             Print lists of devices available under your account
    spot-check          Spot check a Spotter location and time
    spot-data           Export Spotter Data based on Spotter ID & grouped by date

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for specific functionality, simply call it with _help_ switch, e.g.: `pyspotter spot-check -h`. If you didn't install pyspotter, then you can run it just by going to *pyspotter* directory and running `python pyspotter.py [arguments go here]`

## pyspotter Simple CLI for Sofarocean API
The tool is designed to interact with the SofarOcean API, for now this is focused only on the spotter endpoints.

### pyspotter auth
This allows you to save your authentication token, this is then used for authentication for requests. This uses your email and your password to fetch the token.

``` pyspotter auth```

![pyspotter_auth](https://user-images.githubusercontent.com/6677629/147421243-6ca937c4-9614-42ae-9b49-82b3b2d4e286.gif)

### pyspotter reset
For some reason if you need to reset your token , this will allow you to use your current authentication to reset and fetch your new token. This requires no user input

```pyspotter reset```

![pyspotter_reset](https://user-images.githubusercontent.com/6677629/147421249-f2a7ceeb-7d24-41dd-bb50-6bef30913dbc.gif)

### pyspotter devlist
This will simply print the names of all devices to which you have access, instead of trying to remember the list. This tool requires no user input.

```
usage: pyspotter devlist [-h]

optional arguments:
  -h, --help  show this help message and exit

```

usage is simply

```pyspotter devlist```


### pyspotter spotcheck
This tool is built to fetch simply the latest information from the spotter including battery, humidity, power and lat long. Since these spotter can move across multiple time zones, it uses the lat long to estimate the time zone and converts the UTC time to local time for the spotter.

![pyspotter_devices](https://user-images.githubusercontent.com/6677629/147421382-138a03b9-d2e1-4f55-92be-15f88e1ac9e5.gif)

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


### pyspotter spotdata
This tool was designed to get the datasets out of the spotter. It seems that API currently limited temporal data, and the best way to group seemed to be using dates. This script uses the result JSON objects, and adds a date field from the timestamp to make the grouping easy, since timestamps are unique. This then writes these CSV file with column headers and can export both wind and wave data as needed.

![pyspotter_spot-data](https://user-images.githubusercontent.com/6677629/147421473-c3833f2b-8e0e-4188-af88-dd19f30eb74d.gif)

```
usage: pyspotter spot-data [-h] --sid SID --dtype DTYPE --folder FOLDER

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Spotter ID
  --dtype DTYPE    Data type: wind/wave/sst
  --folder FOLDER  Folder to export CSV data

```

Sample setup would be

```
pyspotter spot-data --sid 1234 --dtype wave --folder "full path to folder"
```


## Changelog

#### v0.0.5
- added sea surface temperature parsing for spot data
- minor general improvements

#### v0.0.4
- added spot id to spot data export and metadata
- gracefully handles missing data and better error handling
- general improvements

#### v0.0.3
- added spot check tool to get latest info about spotter
- spot data now exports CSV after grouping by date
- general improvements

#### v0.0.2
- added time zone parser from spotter lat long
- now prints UTC and local time for spotter
- pretty prints output
