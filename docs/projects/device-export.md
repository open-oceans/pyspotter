# Data export

This tool was designed to get the datasets out of the spotter. It seems that API currently limited temporal data, and the best way to group seemed to be using dates. This script uses the result JSON objects, and adds a date field from the timestamp to make the grouping easy, since timestamps are unique. This then writes these CSV file with column headers and can export both wind and wave data as needed.

![pyspotter_spotdata](https://github.com/open-oceans/pyspotter/assets/6677629/78f1a1d7-febc-4c97-9e93-b6a99355f6bd)

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
