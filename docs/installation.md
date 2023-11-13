# General Installation

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

usage: pyspotter [-h] {readme,auth,reset,devlist,spot-check,spot-data,snapshot,snapshot-latest} ...

Simple CLI for Sofarocean API

positional arguments:
  {readme,auth,reset,devlist,spot-check,spot-data,snapshot,snapshot-latest}
    readme              Go to the web based pyspotter cli readme page
    auth                Authenticates and saves your API token
    reset               Regenerates your API token
    devlist             Print lists of devices available under your account
    spot-check          Spot check a Spotter location and time
    spot-data           Export Spotter Data based on Spotter ID & grouped by date
    snapshot            Saves the last 14 day data for a single or global spotters
    snapshot-latest     Saves the latest wind/wave data from global spotters

options:
  -h, --help            show this help message and exit
```
