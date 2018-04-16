# check_graylog_throughput
Nagios check to monitor graylog throughput in messages per second.<br>
(Python Version 2.7)

## Install required python packages
`pip install requests`

## Usage
`python check_graylog_throughput.py --help`
```
usage: check_graylog_throughput.py [-h] [--version] -H HOST -u USER -p
                                   PASSWORD -w WARNING -c CRITICAL [-f]

Check graylog throughput in messages per second.

Arguments:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
  -H HOST      gralog URL
  -u USER      API username
  -p PASSWORD  API passowrd
  -w WARNING   warning level
  -c CRITICAL  critical level
  -f           enable performance data output

Examples:
  check_graylog_throughput.py -H "http://graylog-server:9000" -u USER -p PASS -w 400 -c 500
  check_graylog_throughput.py -H "https://192.168.56.15:9000" -u USER -p PASS -w 100 -c 150 -f
```
