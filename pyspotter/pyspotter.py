#!/usr/bin/python
# -*- coding: utf-8 -*-

__copyright__ = """

MIT License

Copyright (c) 2021-2024 Samapriya Roy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


"""
__license__ = "MIT License"

import argparse
import csv
import datetime
import getpass
import json
import logging
import os
import sys
import time
from itertools import groupby
from os.path import expanduser

import pandas as pd
import pkg_resources
import pytz
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from dateutil.relativedelta import *
from timezonefinder import TimezoneFinder

# Set a custom log formatter
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

class Solution:
    def compareVersion(self, version1, version2):
        versions1 = [int(v) for v in version1.split(".")]
        versions2 = [int(v) for v in version2.split(".")]
        for i in range(max(len(versions1), len(versions2))):
            v1 = versions1[i] if i < len(versions1) else 0
            v2 = versions2[i] if i < len(versions2) else 0
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0


ob1 = Solution()

# Get package version
def pyspotter_version():
    url = "https://pypi.org/project/pyspotter/"
    source = requests.get(url)
    html_content = source.text
    soup = BeautifulSoup(html_content, "html.parser")
    company = soup.find("h1")
    vcheck = ob1.compareVersion(
        company.string.strip().split(" ")[-1],
        pkg_resources.get_distribution("pyspotter").version,
    )
    if vcheck == 1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Current version of pyspotter is {} upgrade to lastest version: {}".format(
                pkg_resources.get_distribution("pyspotter").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )
    elif vcheck == -1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Possibly running staging code {} compared to pypi release {}".format(
                pkg_resources.get_distribution("pyspotter").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )


pyspotter_version()

# set credentials
def auth(usr):
    headers = {
        "authority": "api.sofarocean.com",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://weather.sofarocean.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://weather.sofarocean.com/",
        "accept-language": "en-US,en;q=0.9",
    }
    home = expanduser("~/sofarocean.json")
    if usr is None:
        usr = input("Enter email: ")
    pwd = getpass.getpass("Enter password: ")
    data = {"username": usr, "password": pwd, "skipRedirect": "true"}

    response = requests.post(
        "https://api.sofarocean.com/login/", headers=headers, data=data
    )
    if response.status_code == 200:
        print("Authentication successful")
        data = {"token": response.json()["token"]}
        with open(home, "w") as outfile:
            json.dump(data, outfile)
    else:
        print(f"Authentication failed with error {response.status_code}")


def auth_from_parser(args):
    auth(usr=args.username)


def reset():
    home = expanduser("~/sofarocean.json")
    usr = input("Enter email: ")
    if not os.path.exists(home):
        auth(usr)
        with open(home) as json_file:
            data = json.load(json_file)
            token = data.get("token")
    else:
        with open(home) as json_file:
            data = json.load(json_file)
            token = data.get("token")
    headers = {
        "token": token,
    }
    response = requests.post(
        f"https://api.sofarocean.com/users/{usr}/tokens/", headers=headers
    )
    if response.status_code == 200:
        print("Token reset successful")
        data = {"token": response.json()["token"]}
        with open(home, "w") as outfile:
            json.dump(data, outfile)
    else:
        print("Token reset failed")


def reset_from_parser(args):
    reset()


def tokenize():
    home = expanduser("~/sofarocean.json")
    if not os.path.exists(home):
        auth(usr=None)
        with open(home) as json_file:
            data = json.load(json_file)
            token = data.get("token")
    else:
        with open(home) as json_file:
            data = json.load(json_file)
            token = data.get("token")
    return token


def devlist():
    headers = {
        "token": tokenize(),
    }
    response = requests.get("https://api.sofarocean.com/api/devices", headers=headers)
    response = response.json()
    print(f"Total of {response['message']}" + "\n")
    for device in response["data"]["devices"]:
        print(device["spotterId"])


def devlist_from_parser(args):
    devlist()

def marine_dashboard():
    global_spotter_list = []
    headers = {
        "token": tokenize(),
    }
    params = {
        'includeWindData': 'true',
    }

    response = requests.get('https://api.sofarocean.com/oceans-api/latest-data', params=params, headers=headers)
    for spotter_results in response.json()['data']:
        global_spotter_list.append(spotter_results)
    return global_spotter_list

def datetime_to_epoch_milliseconds(dt):
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
    delta = dt - epoch
    return int(delta.total_seconds() * 1000)

def marine_global(sid,exp):
    master_dashboard_ids = marine_dashboard()
    headers = {
        "token": tokenize(),
    }
    end = datetime.datetime.utcnow()
    #end = end.replace(hour=0, minute=0, second=0, microsecond=0)
    start = end + relativedelta(days=-15)
    end = end.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    start = start.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    logging.info(
        f"Searching between Start date {str(start)} and End date {str(end)}"
    )
    st = str(start).split('T')[0]
    et = str(end).split('T')[0]
    final_path = os.path.join(exp,f"{sid}_{st}_{et}.csv")
    global_df_list =[]
    if not os.path.exists(final_path):
        try:
            if sid=="global":
                for i,sid in enumerate(master_dashboard_ids):
                    response = requests.get(
                        f'https://api.sofarocean.com/oceans-api/wave-data?spotterId={sid}&startDate={start}&endDate={end}',
                        headers=headers,
                    )
                    if response.status_code == 200 and len(response.json()['data']['waves'])>0:
                        print(f"Processed {i} of {len(master_dashboard_ids)} records",end="\r")
                        #geojson_data = json.dumps(response.json(), indent=2)
                        df = pd.DataFrame(response.json()['data']['waves'])
                        df["timestamp"] = pd.to_datetime(df["timestamp"])
                        df["system:time_start"] = df["timestamp"].apply(
                            datetime_to_epoch_milliseconds
                        )
                        global_df_list.append(df)
            else:
                response = requests.get(
                    f'https://api.sofarocean.com/oceans-api/wave-data?spotterId={sid}&startDate={start}&endDate={end}',
                    headers=headers,
                )
                logging.info(f"Found a total of {len(response.json()['data']['waves'])} records")
                #geojson_data = json.dumps(response.json(), indent=2)
                df = pd.DataFrame(response.json()['data']['waves'])
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df["system:time_start"] = df["timestamp"].apply(
                    datetime_to_epoch_milliseconds
                )
                global_df_list.append(df)
            global_df = pd.concat(global_df_list, ignore_index=True)
            global_cleaned = global_df.dropna()
            global_cleaned.to_csv(final_path, index=False)
            logging.info(f"Wrote {global_cleaned.shape[0]} records to csv {os.path.basename(final_path)}")
        except Exception as error:
            logging.error(error)
    else:
        logging.info(f"Marine dashboard export for {sid} already exists at {os.path.basename(final_path)}: SKIPPING")

#marine_global(sid='global',exp=r'C:\tmp\aqua')
#marine_info(sid='SPOT-30168D',exp=r'C:\tmp\aqua')
def global_snapshot_from_parser(args):
    marine_global(spot_id=args.sid,exp=args.export)

def spot_check(spot_id):
    if not spot_id.startswith("SPOT-"):
        spot_id = f"SPOT-{spot_id}"
    dic = {}
    obj = TimezoneFinder()
    headers = {
        "token": tokenize(),
    }
    response = requests.get(
        f"https://api.sofarocean.com/api/latest-data?spotterId={spot_id}",
        headers=headers,
    )
    if response.status_code == 200:
        spotter = response.json()
        print(f"Fetching info for Spotter {spot_id}" + "\n")
        for key, value in spotter["data"].items():
            if key != "frequencyData" and key != "track" and key != "waves":
                dic[key] = value
            # print(key,value)
        latitude = spotter["data"]["waves"][-1]["latitude"]
        longitude = spotter["data"]["waves"][-1]["longitude"]
        time_zone = obj.timezone_at(lat=float(latitude), lng=float(longitude))
        tz = pytz.timezone(time_zone)
        now_utc = parser.parse(spotter["data"]["waves"][-1]["timestamp"])
        now_kl = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)
        dic["last updated (UTC time)"] = str(now_utc)
        dic["last updated (spotter local time)"] = str(now_kl)
        dic["latitude"] = spotter["data"]["waves"][-1]["latitude"]
        dic["longitude"] = spotter["data"]["waves"][-1]["longitude"]
        print(json.dumps(dic, indent=2, sort_keys=False))
    else:
        print(
            f"Spot check failed with error code {response.status_code}: {response.json()['message']}"
        )


def spotcheck_from_parser(args):
    spot_check(spot_id=args.sid)


def spot_data(spot_id, dtype, folder):  #'SPOT-0222'
    waves_list = []
    wind_list = []
    sst_list = []
    if not spot_id.startswith("SPOT-"):
        spot_id = f"SPOT-{spot_id}"
    obj = TimezoneFinder()
    params = {
        "spotterId": [spot_id],
        "includeSurfaceTempData": True,
        "includeWindData": True,
    }
    headers = {
        "token": tokenize(),
    }
    response = requests.get(
        "https://api.sofarocean.com/api/wave-data", headers=headers, params=params
    )
    if response.status_code == 200:
        spotter = response.json()
        print("\n" + f"Fetching info for Spotter {spot_id}" + "\n")
        if (
            not "surfaceTemp" in spotter["data"]
            or len(spotter["data"]["surfaceTemp"]) == 0
            and dtype == "sst"
        ):
            sys.exit("No surfaceTemp data found")
        else:
            for readings in spotter["data"]["surfaceTemp"]:
                readings["date"] = readings["timestamp"].split("T")[0]
                readings["spotter_id"] = spot_id
                sst_list.append(readings)
        if (
            not "waves" in spotter["data"]
            or len(spotter["data"]["waves"]) == 0
            and dtype == "wave"
        ):
            sys.exit("No waves data found")
        else:
            for readings in spotter["data"]["waves"]:
                readings["date"] = readings["timestamp"].split("T")[0]
                readings["spotter_id"] = spot_id
                waves_list.append(readings)
        if (
            not "wind" in spotter["data"]
            or len(spotter["data"]["wind"]) == 0
            and dtype == "wind"
        ):
            sys.exit("No wind data found")
        else:
            for readings in spotter["data"]["wind"]:
                readings["date"] = readings["timestamp"].split("T")[0]
                readings["spotter_id"] = spot_id
                wind_list.append(readings)
    else:
        sys.exit(
            f"Failed with status_code: {response.status_code}: {response.json()['message']}"
        )

    if dtype == "wave":
        csv_columns = [
            "significantWaveHeight",
            "peakPeriod",
            "meanPeriod",
            "peakDirection",
            "peakDirectionalSpread",
            "meanDirection",
            "meanDirectionalSpread",
            "timestamp",
            "latitude",
            "longitude",
            "date",
            "spotter_id",
        ]
        main_list = waves_list
    elif dtype == "wind":
        csv_columns = [
            "speed",
            "direction",
            "seasurfaceId",
            "latitude",
            "longitude",
            "timestamp",
            "date",
            "spotter_id",
        ]
        main_list = wind_list
    elif dtype == "sst":
        csv_columns = [
            "degrees",
            "latitude",
            "longitude",
            "timestamp",
            "date",
            "spotter_id",
        ]
        main_list = sst_list
    # define a fuction for key
    def key_func(k):
        return k["date"]

    # sort INFO data by 'company' key.
    INFO = sorted(main_list, key=key_func)

    for key, value in groupby(INFO, key_func):
        print(f"Processing {spot_id}_{key}_{dtype}.csv")
        dict_data = list(value)
        try:
            with open(
                os.path.join(folder, f"{spot_id}_{key}_{dtype}.csv"), "w"
            ) as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=csv_columns, delimiter=",", lineterminator="\n"
                )
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


def spot_data_from_parser(args):
    spot_data(spot_id=args.sid, dtype=args.dtype, folder=args.folder)


def main(args=None):
    parser = argparse.ArgumentParser(description="Simple CLI for Sofarocean API")
    subparsers = parser.add_subparsers()

    parser_auth = subparsers.add_parser(
        "auth", help="Authenticates and saves your API token"
    )
    optional_named = parser_auth.add_argument_group("Optional named arguments")
    optional_named.add_argument("--username", help="Username", default=None)
    parser_auth.set_defaults(func=auth_from_parser)

    parser_reset = subparsers.add_parser("reset", help="Regenerates your API token")
    parser_reset.set_defaults(func=reset_from_parser)

    parser_devlist = subparsers.add_parser(
        "devlist", help="Print lists of devices available under your account"
    )
    parser_devlist.set_defaults(func=devlist_from_parser)

    parser_spotcheck = subparsers.add_parser(
        "spot-check", help="Spot check a Spotter location and time"
    )
    required_named = parser_spotcheck.add_argument_group("Required named arguments.")
    required_named.add_argument("--sid", help="Spotter ID", required=True)
    parser_spotcheck.set_defaults(func=spotcheck_from_parser)

    parser_spot_data = subparsers.add_parser(
        "spot-data", help="Export Spotter Data based on Spotter ID & grouped by date"
    )
    required_named = parser_spot_data.add_argument_group("Required named arguments.")
    required_named.add_argument("--sid", help="Spotter ID", required=True)
    required_named.add_argument(
        "--dtype", help="Data type: wind/wave/sst", required=True
    )
    required_named.add_argument(
        "--folder", help="Folder to export CSV data", required=True
    )
    parser_spot_data.set_defaults(func=spot_data_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
