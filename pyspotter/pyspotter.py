#!/usr/bin/python
# -*- coding: utf-8 -*-

__copyright__ = """

MIT License

Copyright (c) 2021 Samapriya Roy

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

import requests
import json
import sys
import pkg_resources
import argparse
import time
import getpass
import os
import pytz
from dateutil import parser
from os.path import expanduser
from bs4 import BeautifulSoup
from timezonefinder import TimezoneFinder


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
    print(f"Total of {response['message']}"+'\n')
    for device in response['data']['devices']:
        print(device['spotterId'])


def devlist_from_parser(args):
    devlist()


def spot_data(spot_id):  #'SPOT-0222'
    obj = TimezoneFinder()
    params = {"spotterId": [spot_id], "includeSurfaceTempData": True}
    headers = {
        "token": tokenize(),
    }
    response = requests.get(
        "https://api.sofarocean.com/api/wave-data", headers=headers, params=params
    )
    if response.status_code == 200:
        spotter = response.json()
        for segments in spotter['data']['surfaceTemp']:
            print(segments)
        print(f'Fetching info for Spotter {spot_id}'+'\n')
        latitude = spotter["data"]["waves"][-1]["latitude"]
        longitude = spotter["data"]["waves"][-1]["longitude"]
        time_zone = obj.timezone_at(lat=float(latitude), lng=float(longitude))
        tz = pytz.timezone(time_zone)
        now_utc = parser.parse(spotter["data"]["waves"][-1]["timestamp"])
        now_kl = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)
        print(f'Last updated UTC time from spotter {spot_id} : {now_utc}')
        print(f'Last updated local time from spotter {spot_id} : {now_kl}')
        print(f'Last location from spotter {spot_id} lat,long: {spotter["data"]["waves"][-1]["latitude"]},{spotter["data"]["waves"][-1]["longitude"]}')
        time.sleep(5) # add a time lag to read time and location info
        for readings in spotter["data"]["waves"]:
            print(json.dumps(readings,indent=2))


def spot_data_from_parser(args):
    spot_data(spot_id=args.sid)


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

    parser_spot_data = subparsers.add_parser(
        "spot_data", help="Print Spotter Data based on Spotter ID"
    )
    optional_named = parser_spot_data.add_argument_group("Optional named arguments")
    optional_named.add_argument("--sid", help="Spotter ID", default=None)
    parser_spot_data.set_defaults(func=spot_data_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
