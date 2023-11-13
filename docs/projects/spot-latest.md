# Global latest Snapshot

This tool allows the user to create the latest data snapshot of global spotter database. An extra column with system:time_start is added where the timestamp is converted to epoch time in milliseconds. This tool will accept dtype/data type which can be wave/wind.

![pyspotter_snapshot_latest](https://github.com/open-oceans/pyspotter/assets/6677629/8a447f60-9f73-42fb-8234-aa2e2902f37d)

```
pyspotter snapshot-latest -h
usage: pyspotter snapshot-latest [-h] --export EXPORT --dtype DTYPE

options:
  -h, --help       show this help message and exit

Required named arguments.:
  --export EXPORT  Full path to folder to export results
  --dtype DTYPE    Data type wind/wave
```
