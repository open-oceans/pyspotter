# Global biweekly Snapshot

This tool is designed to fetch a 14 day rolling biweekly snapshot of global spotter database. This can accept a single spotter id or can simply take the export folder to create the global snapshot CSV file. An extra column with system:time_start is added where the timestamp is converted to epoch time in milliseconds. Current export only includes wave data.

![pyspotter_snapshot](https://github.com/open-oceans/pyspotter/assets/6677629/7875c21e-6e84-41e7-b246-7ccaa84d18ef)

```
pyspotter snapshot -h
usage: pyspotter snapshot [-h] --export EXPORT [--sid SID]

options:
  -h, --help       show this help message and exit

Required named arguments.:
  --export EXPORT  Full path to folder to export results

Optional named arguments:
  --sid SID        Spotter ID
```
