#!/usr/bin/env python
"""Tufts Computer Lab Attendance Checker.

Usage:
  ./checkAttendance.py

Options:
  -h, --help  Show this screen.
"""
# TODO: add note about making sure to log into each machine and accept the host key
from docopt import docopt

machines = {
  "116": ["lab116a", "lab116b", "lab116c", "lab116d", "lab116e", "lab116f", "lab116g", "lab116h", "lab116i", "lab116j", "lab116k", "lab116l", "lab116m", "lab116n", "lab116o", "lab116p", "lab116q", "lab116r", "lab116s", "lab116t", "lab116u", "lab116v", "lab116w", "lab116x"]
  , "118": ["lab118a", "lab118b", "lab118c", "lab118d", "lab118e", "lab118f", "lab118g", "lab118h", "lab118i", "lab118j", "lab118k", "lab118l", "lab118m", "lab118n", "lab118o", "lab118p", "lab118q", "lab118r", "lab118s", "lab118t", "lab118u", "lab118v", "lab118w", "lab118x"]
  , "120": ["lab120a", "lab120b", "lab120c", "lab120d", "lab120e", "lab120f", "lab120g", "lab120h", "lab120i", "lab120j", "lab120k", "lab120l", "lab120m", "lab120n", "lab120o", "lab120p", "lab120q", "lab120r", "lab120s", "lab120t", "lab120u", "lab120v"]
}

# ssh lab116a.cs.tufts.edu last




















if __name__ == "__main__":
  arguments = docopt(__doc__, version="Attendance Checker v1.0")
