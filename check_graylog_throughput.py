#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  Bernhard Hörl www.bernhardhoerl.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import argparse
import requests
import urllib3

from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth


def get_throughput (host, user, password, warning, critical, perfdata):

    urllib3.disable_warnings()

    url = host + "/api/system/throughput"
    r = requests.get(url, verify=False)
    s_auth = r.headers.get('www-authenticate')

    if s_auth and 'basic' in s_auth.lower():
        r = requests.get(url, auth=HTTPBasicAuth(user, password), verify=False)
    elif s_auth and 'digest' in s_auth.lower():
        r = requests.get(url, auth=HTTPDigestAuth(user, password), verify=False)

    if r.status_code == 200:
        data = r.json()
        throughput = data["throughput"]
    else:
        print "HTTP Error: " + str(r.status_code)
        sys.exit(1)

    throughput_msg = str(throughput) + " msg/s"
    throughput_msg_perfdata = str(throughput) + " msg/s | msg/s=" + str(throughput)

    if throughput > critical:
        if perfdata:
            print "CRITICAL: " + throughput_msg_perfdata
            sys.exit(2)
        print "CRITICAL: " + throughput_msg
        sys.exit(2)
    elif throughput > warning:
        if perfdata:
            print "WARNING: " + throughput_msg_perfdata
            sys.exit(1)
        print "WARNING: " + throughput_msg
        sys.exit(1)

    if perfdata:
        print "OK: " + throughput_msg_perfdata
        sys.exit(0)
    else:
        print "OK: " + throughput_msg
        sys.exit(0)


def main ():

    parser = argparse.ArgumentParser(
        description="Check graylog throughput in messages per second.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=('''Examples:
  check_graylog_throughput.py -H "http://graylog-server:9000" -u USER -p PASS -w 400 -c 500
  check_graylog_throughput.py -H "https://192.168.56.15:9000" -u USER -p PASS -w 100 -c 150 -f
        '''))

    parser._optionals.title = "Arguments"

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    parser.add_argument("-H",
                        dest="host", required=True,
                        help="gralog URL")
    parser.add_argument("-u",
                        dest="user", required=True,
                        help="API username")
    parser.add_argument("-p",
                        dest="password", required=True,
                        help="API passowrd")
    parser.add_argument("-w",
                        dest="warning", type=float, required=True,
                        help="warning level")
    parser.add_argument("-c",
                        dest="critical", type=float, required=True,
                        help="critical level")
    parser.add_argument("-f",
                        action="store_true", dest="perfdata",
                        help="enable performance data output")

    args = parser.parse_args()

    if args.critical < args.warning:
        parser.print_usage()
        print __file__ + ": error: value of cirtical must be higher than warning"
        sys.exit(3)

    # https://stackoverflow.com/questions/10408826/remove-leading-and-trailing-slash
    get_throughput(args.host.strip("/"), args.user, args.password, args.warning, args.critical, args.perfdata)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print str(error)
        sys.exit(3)
