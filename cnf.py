#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""Config module for servermonitor."""

import ConfigParser
import sys
import os

def getConfig():
    """ Find and parse configfile. """

    # Ge
    configpath = os.path.join(os.path.expanduser("~"), ".servermonitor.rc")
    if os.path.isfile(configpath):
        config
