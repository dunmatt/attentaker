#!/usr/bin/env python
"""Tufts Computer Lab Attendance Checker.

Usage:
  ./checkAttendance.py [-l <lab>] [-d <date>] [--debug | --verbose]
  ./checkAttendance.py [-l <lab>] [-t <time>] [--debug | --verbose]

Options:
  -t <time>, --at=<time>    Check the attendance for the hour leading up to <time> (in zero padded 24 hour time).  [default: now]
  -d <date>, --on=<date>    Check the attendance for the given date (in YYYY-MM-DD).
  --debug                   Print debugging info.
  -h, --help                Show this screen.
  -l <lab>, --lab=<lab>     Which lab to check the attendance of?  [default: all]
  -v, --verbose             Verbose output.
"""
# TODO: add note about making sure to log into each machine and accept the host key
# TODO: consider instead adding the ability to populate their known_hosts for them

import logging
import re

from datetime import date, datetime, timedelta
from docopt import docopt
from subprocess import check_output as run

machines = {
  "116": ["lab116a", "lab116b", "lab116c", "lab116d", "lab116e", "lab116f", "lab116g", "lab116h", "lab116i", "lab116j", "lab116k", "lab116l", "lab116m", "lab116n", "lab116o", "lab116p", "lab116q", "lab116r", "lab116s", "lab116t", "lab116u", "lab116v", "lab116w", "lab116x"]
  , "118": ["lab118a", "lab118b", "lab118c", "lab118d", "lab118e", "lab118f", "lab118g", "lab118h", "lab118i", "lab118j", "lab118k", "lab118l", "lab118m", "lab118n", "lab118o", "lab118p", "lab118q", "lab118r", "lab118s", "lab118t", "lab118u", "lab118v", "lab118w", "lab118x"]
  , "120": ["lab120a", "lab120b", "lab120c", "lab120d", "lab120e", "lab120f", "lab120g", "lab120h", "lab120i", "lab120j", "lab120k", "lab120l", "lab120m", "lab120n", "lab120o", "lab120p", "lab120q", "lab120r", "lab120s", "lab120t", "lab120u", "lab120v"]
  # , "debug": ["lab116a"]
  , "debug": ["localhost"]
}

def getMachineList(lab):
  if lab in machines:
    return machines[lab]
  elif lab == "all":
    return machines["116"] + machines["118"] + machines["120"]
  else:
    logging.error("Unknown lab, valid options are: all, %s" % ", ".join(sorted(machines.keys())))

def stripTabs(str):
  return str.replace("\t", "")

def process(raw_output):
  for line in raw_output.split("\n"):
    match = re.search("^(\w+)\W.+?:0.+?\W([A-Z][a-z]{2}\s[A-Z][a-z]{2}\s+\d\d?)\s(\d\d?:\d\d).{3}(still|\d\d?:\d\d)", line)
    if match:
      logging.debug(line)
      username = stripTabs(match.group(1))
      loginTimeStr = "%s %s %s" % (date.today().year, match.group(2), match.group(3))
      loginTime = datetime.strptime(loginTimeStr, "%Y %a %b %d %H:%M")
      logoutTimeStr = "%s %s %s" % (date.today().year, match.group(2), match.group(4))
      logoutTime = datetime.now() if "still" in match.group(4) else datetime.strptime(logoutTimeStr, "%Y %a %b %d %H:%M")
      yield (username, loginTime, logoutTime)

def getLogins(machines, timeWindowContains):
  results = set()
  if not machines:
    return results
  for machine in machines:
    logging.info("Scanning %s" % machine)
    try:
      raw_output = run(["ssh", machine, "last"])
      for entry in process(raw_output):
        if timeWindowContains(entry):
          results.add(entry[0])
    except:
      logging.info("Couldn't reach %s" % machine)
  return results


if __name__ == "__main__":
  arguments = docopt(__doc__, version="Attendance Checker v1.1")
  if arguments["--verbose"]:
    logging.basicConfig(level=logging.INFO)
  if arguments["--debug"]:
    logging.basicConfig(level=logging.DEBUG)
  now = datetime.now()
  # date parsing, recipe for pain, for details see the second half of http://www.youtube.com/watch?v=l3nPJ-yK-LU
  dateArg = datetime.strptime(arguments["--on"], "%Y-%m-%d").date() if "--on" in arguments and arguments["--on"] else None
  timeArg = now if arguments["--at"] == "now" else datetime.strptime(now.date().isoformat()+" "+arguments["--at"], "%Y-%m-%d %H:%M")

  def inPreviousHour(query):
    return now - timedelta(0, 3600) <= query[2] and query[1] <= now

  def onDay(query):
    return dateArg == query[1].date()

  machines = getMachineList(arguments["--lab"])
  for username in getLogins(machines, onDay if dateArg else inPreviousHour):
    print username
  # from dry_run_data import data
  # for t in process(data):
  #   print t
